/*
 * repka_pud_driver_production.c
 * Полноценный, безопасный драйвер для управления PUD.
 * Не предоставляет прямого доступа к памяти, работает через IOCTL.
 */

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/version.h>
#include <linux/uaccess.h>
#include <linux/io.h>
#include <linux/cdev.h>
#include <linux/device.h>
#include <linux/slab.h> // Для kzalloc

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Semion Platcev 2025");
MODULE_DESCRIPTION("Production-ready Repka Pi PUD control driver");

#define DEVICE_NAME "repka_pud"
#define CLASS_NAME  "repka_gpio"

// --- Структура для команд ---
struct pud_command {
    unsigned long addr;
    unsigned int shift;
    unsigned int code;
};
// Определяем универсальную IOCTL команду с "магическим" числом 'R'
#define REPKA_PUD_IOC_MAGIC 'R'
#define IOCTL_PUD_RMW _IOW(REPKA_PUD_IOC_MAGIC, 1, struct pud_command)

// --- Глобальные переменные ---
static dev_t dev_num;
static struct cdev my_cdev;
static struct class* my_class = NULL;
static struct mutex ioctl_mutex; // Мьютекс для защиты от одновременного доступа

// --- Основная функция-обработчик IOCTL ---
static long my_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
    struct pud_command user_cmd; // Убираем указатель, используем стек
    void __iomem *reg_virt_addr = NULL;
    u32 current_val, new_val;
    long ret = 0;

    // --- ИЗМЕНЕНИЕ ---
    // Упрощаем проверку. Теперь драйвер слушает только команду 0.
    if (cmd != 0) {
        pr_warn("RepkaPUD: Received unknown IOCTL command: %u\n", cmd);
        return -ENOTTY;
    }

    // Блокируем мьютекс, чтобы только один процесс мог работать с регистрами
    if (mutex_lock_interruptible(&ioctl_mutex)) {
        return -ERESTARTSYS;
    }

    // Безопасно копируем данные от пользователя.
    // Вместо выделения памяти (kzalloc) используем локальную переменную.
    if (copy_from_user(&user_cmd, (struct pud_command __user *)arg, sizeof(user_cmd))) {
        pr_err("RepkaPUD: Failed to copy command from user space\n");
        ret = -EFAULT;
        goto out_unlock; // Переходим сразу к разблокировке мьютекса
    }
    
    // Получаем временный виртуальный адрес
    reg_virt_addr = ioremap(user_cmd.addr, 4);
    if (!reg_virt_addr) {
        pr_err("RepkaPUD: Failed to ioremap address 0x%lx\n", user_cmd.addr);
        ret = -ENOMEM;
        goto out_unlock;
    }

    // --- Цикл Read-Modify-Write ---
    current_val = readl(reg_virt_addr);
    new_val = (current_val & ~(0b11 << user_cmd.shift)) | (user_cmd.code << user_cmd.shift);
    writel(new_val, reg_virt_addr);
    
    iounmap(reg_virt_addr);

    pr_info("RepkaPUD: RMW on 0x%lx. Wrote 0x%x\n", user_cmd.addr, new_val);

out_unlock:
    mutex_unlock(&ioctl_mutex); // Разблокируем мьютекс
    return ret;
}

// --- [БЛОК 6: "Паспорт" драйвера] ---
static const struct file_operations my_fops = {
    .owner = THIS_MODULE,
    .unlocked_ioctl = my_ioctl,
};

// --- [БЛОК 7: Функция инициализации (при загрузке)] ---
static int __init my_init(void) {
    pr_info("RepkaPUD: Loading driver...\n");
    mutex_init(&ioctl_mutex);

    if (alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME) < 0) {
        pr_err("RepkaPUD: Failed to allocate major number\n");
        return -1;
    }
    
 /*
 * УНИВЕРСАЛЬНЫЙ КОД ДЛЯ СОЗДАНИЯ КЛАССА УСТРОЙСТВА
 * Проверяем версию ядра, чтобы использовать правильный API.
 * В ядре 6.4 API для class_create изменился (макрос стал функцией).
 */
#if LINUX_VERSION_CODE >= KERNEL_VERSION(6, 4, 0)
    // Новый API для ядер 6.4 и новее (как на Repka Pi 4)
    my_class = class_create(CLASS_NAME);
#else
    // Старый API для ядер до версии 6.4 (как на Repka Pi 3)
    my_class = class_create(THIS_MODULE, CLASS_NAME);
#endif

    if (IS_ERR(my_class)) {
        unregister_chrdev_region(dev_num, 1);
        pr_err("RepkaPUD: Failed to create device class\n");
        return PTR_ERR(my_class);
    }

    if (IS_ERR(device_create(my_class, NULL, dev_num, NULL, DEVICE_NAME))) {
        class_destroy(my_class);
        unregister_chrdev_region(dev_num, 1);
        pr_err("RepkaPUD: Failed to create the device\n");
        return -1;
    }
    
    cdev_init(&my_cdev, &my_fops);
    if (cdev_add(&my_cdev, dev_num, 1) < 0) {
        device_destroy(my_class, dev_num);
        class_destroy(my_class);
        unregister_chrdev_region(dev_num, 1);
        pr_err("RepkaPUD: Failed to add the cdev\n");
        return -1;
    }
    
    pr_info("RepkaPUD: Driver loaded. Device created at /dev/%s\n", DEVICE_NAME);
    return 0;
}

// --- [БЛОК 8: Функция выхода (при выгрузке)] ---
static void __exit my_exit(void) {
    cdev_del(&my_cdev);
    device_destroy(my_class, dev_num);
    class_destroy(my_class);
    unregister_chrdev_region(dev_num, 1);
    pr_info("RepkaPUD: Driver unloaded.\n");
}

// --- [БЛОК 9: Регистрация функций инициализации и выхода] ---
module_init(my_init);
module_exit(my_exit);