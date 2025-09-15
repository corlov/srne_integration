# Стандартный и надежный Makefile для внешнего модуля ядра
obj-m := repka_pud_driver.o

# Путь к заголовочным файлам ядра
KDIR := /lib/modules/$(shell uname -r)/build

# Текущая рабочая директория
PWD := $(shell pwd)

# Цель по умолчанию (для команды 'make')
default:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

# Цель для очистки
clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean