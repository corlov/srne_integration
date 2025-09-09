--
-- PostgreSQL database dump
--

-- Dumped from database version 14.18 (Ubuntu 14.18-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.18 (Ubuntu 14.18-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: device; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA device;


ALTER SCHEMA device OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: command_history; Type: TABLE; Schema: device; Owner: postgres
--

CREATE TABLE device.command_history (
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    payload jsonb NOT NULL,
    device_id integer NOT NULL,
    err_text character varying,
    status integer DEFAULT 0 NOT NULL,
    id bigint NOT NULL
);


ALTER TABLE device.command_history OWNER TO postgres;

--
-- Name: TABLE command_history; Type: COMMENT; Schema: device; Owner: postgres
--

COMMENT ON TABLE device.command_history IS 'команды отправленные в контроллер СП история';


--
-- Name: COLUMN command_history.payload; Type: COMMENT; Schema: device; Owner: postgres
--

COMMENT ON COLUMN device.command_history.payload IS 'сама команда';


--
-- Name: COLUMN command_history.status; Type: COMMENT; Schema: device; Owner: postgres
--

COMMENT ON COLUMN device.command_history.status IS 'меняет свое значение в течение ЖЦ';


--
-- Name: command_history_id_seq; Type: SEQUENCE; Schema: device; Owner: postgres
--

CREATE SEQUENCE device.command_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE device.command_history_id_seq OWNER TO postgres;

--
-- Name: command_history_id_seq; Type: SEQUENCE OWNED BY; Schema: device; Owner: postgres
--

ALTER SEQUENCE device.command_history_id_seq OWNED BY device.command_history.id;


--
-- Name: complex_settings; Type: TABLE; Schema: device; Owner: postgres
--

CREATE TABLE device.complex_settings (
    id integer NOT NULL,
    param character varying(255) NOT NULL,
    value character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    descr character varying(255),
    type text,
    options jsonb,
    ui_field_order integer
);


ALTER TABLE device.complex_settings OWNER TO postgres;

--
-- Name: TABLE complex_settings; Type: COMMENT; Schema: device; Owner: postgres
--

COMMENT ON TABLE device.complex_settings IS 'настройки комплекса (репки) и прочие настройки статическая таблица';


--
-- Name: complex_settings_id_seq; Type: SEQUENCE; Schema: device; Owner: postgres
--

CREATE SEQUENCE device.complex_settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE device.complex_settings_id_seq OWNER TO postgres;

--
-- Name: complex_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: device; Owner: postgres
--

ALTER SEQUENCE device.complex_settings_id_seq OWNED BY device.complex_settings.id;


--
-- Name: dynamic_information; Type: TABLE; Schema: device; Owner: postgres
--

CREATE TABLE device.dynamic_information (
    id bigint NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    payload jsonb NOT NULL,
    device_id integer DEFAULT 0 NOT NULL
);


ALTER TABLE device.dynamic_information OWNER TO postgres;

--
-- Name: TABLE dynamic_information; Type: COMMENT; Schema: device; Owner: postgres
--

COMMENT ON TABLE device.dynamic_information IS 'информация о значении параметров контроллера СП';


--
-- Name: dynamic_information_id_seq; Type: SEQUENCE; Schema: device; Owner: postgres
--

CREATE SEQUENCE device.dynamic_information_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE device.dynamic_information_id_seq OWNER TO postgres;

--
-- Name: dynamic_information_id_seq; Type: SEQUENCE OWNED BY; Schema: device; Owner: postgres
--

ALTER SEQUENCE device.dynamic_information_id_seq OWNED BY device.dynamic_information.id;


--
-- Name: eeprom_parameter_setting; Type: TABLE; Schema: device; Owner: postgres
--

CREATE TABLE device.eeprom_parameter_setting (
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    payload jsonb NOT NULL,
    device_id integer NOT NULL
);


ALTER TABLE device.eeprom_parameter_setting OWNER TO postgres;

--
-- Name: TABLE eeprom_parameter_setting; Type: COMMENT; Schema: device; Owner: postgres
--

COMMENT ON TABLE device.eeprom_parameter_setting IS 'настройки контроллера СП считанные из его постоянной памяти ЕЕПРОМа';


--
-- Name: event_log; Type: TABLE; Schema: device; Owner: postgres
--

CREATE TABLE device.event_log (
    id integer NOT NULL,
    event_type character varying(50) NOT NULL,
    event_name character varying(100) NOT NULL,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    device_id integer,
    severity character varying(20) DEFAULT 'INFO'::character varying,
    metadata jsonb,
    CONSTRAINT event_log_severity_check CHECK (((severity)::text = ANY ((ARRAY['DEBUG'::character varying, 'INFO'::character varying, 'WARNING'::character varying, 'ERROR'::character varying, 'CRITICAL'::character varying])::text[])))
);


ALTER TABLE device.event_log OWNER TO postgres;

--
-- Name: TABLE event_log; Type: COMMENT; Schema: device; Owner: postgres
--

COMMENT ON TABLE device.event_log IS 'журнал событий комплекса';


--
-- Name: event_log_id_seq; Type: SEQUENCE; Schema: device; Owner: postgres
--

CREATE SEQUENCE device.event_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE device.event_log_id_seq OWNER TO postgres;

--
-- Name: event_log_id_seq; Type: SEQUENCE OWNED BY; Schema: device; Owner: postgres
--

ALTER SEQUENCE device.event_log_id_seq OWNED BY device.event_log.id;


--
-- Name: history; Type: TABLE; Schema: device; Owner: postgres
--

CREATE TABLE device.history (
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    day integer NOT NULL,
    payload jsonb NOT NULL,
    device_id integer NOT NULL,
    actual_date timestamp without time zone
);


ALTER TABLE device.history OWNER TO postgres;

--
-- Name: TABLE history; Type: COMMENT; Schema: device; Owner: postgres
--

COMMENT ON TABLE device.history IS 'история вычитываемая из внутренней памяти контроллера СП - контроллер хранит значения параметров за 1024 суток.';


--
-- Name: system_information; Type: TABLE; Schema: device; Owner: postgres
--

CREATE TABLE device.system_information (
    device_id integer NOT NULL,
    payload jsonb NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE device.system_information OWNER TO postgres;

--
-- Name: TABLE system_information; Type: COMMENT; Schema: device; Owner: postgres
--

COMMENT ON TABLE device.system_information IS 'сист. инф. контроллера СП вычитываемые из него';


--
-- Name: complex_settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.complex_settings (
    id integer NOT NULL,
    param character varying(255) NOT NULL,
    value character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.complex_settings OWNER TO postgres;

--
-- Name: complex_settings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.complex_settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.complex_settings_id_seq OWNER TO postgres;

--
-- Name: complex_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.complex_settings_id_seq OWNED BY public.complex_settings.id;


--
-- Name: command_history id; Type: DEFAULT; Schema: device; Owner: postgres
--

ALTER TABLE ONLY device.command_history ALTER COLUMN id SET DEFAULT nextval('device.command_history_id_seq'::regclass);


--
-- Name: complex_settings id; Type: DEFAULT; Schema: device; Owner: postgres
--

ALTER TABLE ONLY device.complex_settings ALTER COLUMN id SET DEFAULT nextval('device.complex_settings_id_seq'::regclass);


--
-- Name: dynamic_information id; Type: DEFAULT; Schema: device; Owner: postgres
--

ALTER TABLE ONLY device.dynamic_information ALTER COLUMN id SET DEFAULT nextval('device.dynamic_information_id_seq'::regclass);


--
-- Name: event_log id; Type: DEFAULT; Schema: device; Owner: postgres
--

ALTER TABLE ONLY device.event_log ALTER COLUMN id SET DEFAULT nextval('device.event_log_id_seq'::regclass);


--
-- Name: complex_settings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complex_settings ALTER COLUMN id SET DEFAULT nextval('public.complex_settings_id_seq'::regclass);


--
-- Data for Name: command_history; Type: TABLE DATA; Schema: device; Owner: postgres
--

COPY device.command_history (created_at, payload, device_id, err_text, status, id) FROM stdin;
\.


--
-- Data for Name: complex_settings; Type: TABLE DATA; Schema: device; Owner: postgres
--

COPY device.complex_settings (id, param, value, created_at, descr, type, options, ui_field_order) FROM stdin;
13	device_load_working_mode	ручной режим	2025-09-04 22:05:56.955125	Режим работы нагрузки	select	["контроль включения/выключения нагрузки", "выкл. через 1 час", "выкл. через 2 час", "выкл. через 3 час", "выкл. через 4 час", "выкл. через 5 час", "выкл. через 6 час", "выкл. через 7 час", "выкл. через 8 час", "выкл. через 9 час", "выкл. через 10 час", "выкл. через 11 час", "выкл. через 12 час", "выкл. через 13 час", "выкл. через 14 час", "ручной режим", "режим отладки", "включен"]	6
15	solar_panel_state_debounce_seconds	10	2025-09-08 09:46:31.578715	Интервал записи в журнал параметров работы	string	\N	15
9	its_connection_period	60	2025-08-26 14:49:28.06652	Пероид выхода на связь с ИТС:	string	\N	13
8	time_source_addr	pool.ntp.org	2025-08-26 14:49:28.06652	адрес источника точного времени	string	\N	9
4	params_log_period	300	2025-08-25 09:37:37.974177	Частота записы в журнал параметров работы	string	\N	4
6	trafficlight_work_mode	режим 3 (алгоритм)	2025-08-26 14:49:28.06652	Режим работы светофора	select	["режим 1 (1Гц, 500мс)", "режим 2 (1Гц, 100мс)", "режим 3 (алгоритм)", "режим 4 (откл.)"]	7
11	switch_off_modem	false	2025-08-26 14:49:28.06652	Отключать модем после сеанса связи	boolean	\N	11
1	version	1.0.1	2025-08-25 09:37:37.974177	Версия АК	string	\N	1
2	coordinates	55.7558, 37.6173	2025-08-25 09:37:37.974177	местоположение	string	\N	2
7	time_source	RTC	2025-08-26 14:49:28.06652	источник точного времени тип	select	["NTP", "RTC"]	8
3	battery_type	свинцово-кислотный	2025-08-25 09:37:37.974177	тип батареи	select	["ВРЛА", "гелий", "свинцово-кислотный", "литиевый"]	3
5	load_work_mode	откл.	2025-08-26 14:49:28.06652	Режим работы светильника	select	["режим", "откл.", "вкл."]	5
14	commands_debounce_seconds	2	2025-09-08 09:46:28.708981	Интервал между приемом команд	string	\N	14
10	keep_connection_alive	true	2025-08-26 14:49:28.06652	Режим постоянной связи: (да / нет)	boolean	\N	10
12	modem_off_delay	10	2025-08-26 14:49:28.06652	Время удержания модема после связи минут	string	\N	12
\.


--
-- Data for Name: dynamic_information; Type: TABLE DATA; Schema: device; Owner: postgres
--

COPY device.dynamic_information (id, created_at, payload, device_id) FROM stdin;
\.


--
-- Data for Name: eeprom_parameter_setting; Type: TABLE DATA; Schema: device; Owner: postgres
--

COPY device.eeprom_parameter_setting (created_at, payload, device_id) FROM stdin;
2025-09-08 15:58:42.169479	{"ts": 1757336319.1777573, "common": [{"unit": "V", "boostchargingRecoveryVoltage": 132}, {"unit": "V", "overDischargeRecoveryVoltage": 126}, {"unit": "V", "underVoltageWarningLevel": 120}, {"unit": "V", "overDischargeVoltage": 111}, {"unit": "V", "dischargingLimitVoltage": 106}, {"unit": "second", "overDischareTimeDelay": 5}, {"unit": "minute", "equalizingChargingTime": 120}, {"unit": "minute", "boostChargingTime": 120}, {"unit": "day", "equalizingChargingInterval": 30}, {"unit": "mV", "temperatureCompensationFactor": 3}, {"unit": "string", "loadWorkingMode": "Manual mode"}], "battery": [{"unit": "AH", "nominalBatteryCapacity": 200}, {"unit": "V", "systemVoltageSetting": 255}, {"unit": "V", "recognizedVoltage": 2}, {"unit": "string", "batteryType": "sealed"}, {"unit": "V", "overVoltageThreshold": 160}, {"unit": "V", "chargingVoltageLimit": 155}, {"unit": "V", "equalizingChargingVoltage": 146}, {"unit": "V", "boostchargingVoltage": 144}, {"unit": "V", "floatingChargingVoltage": 138}], "lightControl": {"common": [{"unit": "minute", "lightControlDelay": 5}, {"unit": "V", "lightControlVoltage": 5}], "specialPowerControl": [{"unit": "V", "eachNightOnFunctionEnabled": true}, {"unit": "V", "specialPowerControlFunctionEnabled": false}, {"unit": "V", "noChargingBelowZero": false}, {"unit": "V", "charging method": "direct charging"}]}}	2
2025-09-08 15:59:52.185981	{"ts": 1757336389.206558, "common": [{"unit": "V", "boostchargingRecoveryVoltage": 132}, {"unit": "V", "overDischargeRecoveryVoltage": 126}, {"unit": "V", "underVoltageWarningLevel": 120}, {"unit": "V", "overDischargeVoltage": 111}, {"unit": "V", "dischargingLimitVoltage": 106}, {"unit": "second", "overDischareTimeDelay": 5}, {"unit": "minute", "equalizingChargingTime": 120}, {"unit": "minute", "boostChargingTime": 120}, {"unit": "day", "equalizingChargingInterval": 30}, {"unit": "mV", "temperatureCompensationFactor": 3}, {"unit": "string", "loadWorkingMode": "Manual mode"}], "battery": [{"unit": "AH", "nominalBatteryCapacity": 200}, {"unit": "V", "systemVoltageSetting": 255}, {"unit": "V", "recognizedVoltage": 2}, {"unit": "string", "batteryType": "sealed"}, {"unit": "V", "overVoltageThreshold": 160}, {"unit": "V", "chargingVoltageLimit": 155}, {"unit": "V", "equalizingChargingVoltage": 146}, {"unit": "V", "boostchargingVoltage": 144}, {"unit": "V", "floatingChargingVoltage": 138}], "lightControl": {"common": [{"unit": "minute", "lightControlDelay": 5}, {"unit": "V", "lightControlVoltage": 5}], "specialPowerControl": [{"unit": "V", "eachNightOnFunctionEnabled": true}, {"unit": "V", "specialPowerControlFunctionEnabled": false}, {"unit": "V", "noChargingBelowZero": false}, {"unit": "V", "charging method": "direct charging"}]}}	2
2025-09-08 16:00:40.249439	{"ts": 1757336437.2617185, "common": [{"unit": "V", "boostchargingRecoveryVoltage": 132}, {"unit": "V", "overDischargeRecoveryVoltage": 126}, {"unit": "V", "underVoltageWarningLevel": 120}, {"unit": "V", "overDischargeVoltage": 111}, {"unit": "V", "dischargingLimitVoltage": 106}, {"unit": "second", "overDischareTimeDelay": 5}, {"unit": "minute", "equalizingChargingTime": 120}, {"unit": "minute", "boostChargingTime": 120}, {"unit": "day", "equalizingChargingInterval": 30}, {"unit": "mV", "temperatureCompensationFactor": 3}, {"unit": "string", "loadWorkingMode": "Manual mode"}], "battery": [{"unit": "AH", "nominalBatteryCapacity": 200}, {"unit": "V", "systemVoltageSetting": 255}, {"unit": "V", "recognizedVoltage": 2}, {"unit": "string", "batteryType": "sealed"}, {"unit": "V", "overVoltageThreshold": 160}, {"unit": "V", "chargingVoltageLimit": 155}, {"unit": "V", "equalizingChargingVoltage": 146}, {"unit": "V", "boostchargingVoltage": 144}, {"unit": "V", "floatingChargingVoltage": 138}], "lightControl": {"common": [{"unit": "minute", "lightControlDelay": 5}, {"unit": "V", "lightControlVoltage": 5}], "specialPowerControl": [{"unit": "V", "eachNightOnFunctionEnabled": true}, {"unit": "V", "specialPowerControlFunctionEnabled": false}, {"unit": "V", "noChargingBelowZero": false}, {"unit": "V", "charging method": "direct charging"}]}}	2
2025-09-08 16:01:12.733559	{"ts": 1757336469.7390187, "common": [{"unit": "V", "boostchargingRecoveryVoltage": 132}, {"unit": "V", "overDischargeRecoveryVoltage": 126}, {"unit": "V", "underVoltageWarningLevel": 120}, {"unit": "V", "overDischargeVoltage": 111}, {"unit": "V", "dischargingLimitVoltage": 106}, {"unit": "second", "overDischareTimeDelay": 5}, {"unit": "minute", "equalizingChargingTime": 120}, {"unit": "minute", "boostChargingTime": 120}, {"unit": "day", "equalizingChargingInterval": 30}, {"unit": "mV", "temperatureCompensationFactor": 3}, {"unit": "string", "loadWorkingMode": "Manual mode"}], "battery": [{"unit": "AH", "nominalBatteryCapacity": 200}, {"unit": "V", "systemVoltageSetting": 255}, {"unit": "V", "recognizedVoltage": 2}, {"unit": "string", "batteryType": "sealed"}, {"unit": "V", "overVoltageThreshold": 160}, {"unit": "V", "chargingVoltageLimit": 155}, {"unit": "V", "equalizingChargingVoltage": 146}, {"unit": "V", "boostchargingVoltage": 144}, {"unit": "V", "floatingChargingVoltage": 138}], "lightControl": {"common": [{"unit": "minute", "lightControlDelay": 5}, {"unit": "V", "lightControlVoltage": 5}], "specialPowerControl": [{"unit": "V", "eachNightOnFunctionEnabled": true}, {"unit": "V", "specialPowerControlFunctionEnabled": false}, {"unit": "V", "noChargingBelowZero": false}, {"unit": "V", "charging method": "direct charging"}]}}	2
2025-09-08 16:02:11.226782	{"ts": 1757336528.2299356, "common": [{"unit": "V", "boostchargingRecoveryVoltage": 132}, {"unit": "V", "overDischargeRecoveryVoltage": 126}, {"unit": "V", "underVoltageWarningLevel": 120}, {"unit": "V", "overDischargeVoltage": 111}, {"unit": "V", "dischargingLimitVoltage": 106}, {"unit": "second", "overDischareTimeDelay": 5}, {"unit": "minute", "equalizingChargingTime": 120}, {"unit": "minute", "boostChargingTime": 120}, {"unit": "day", "equalizingChargingInterval": 30}, {"unit": "mV", "temperatureCompensationFactor": 3}, {"unit": "string", "loadWorkingMode": "Manual mode"}], "battery": [{"unit": "AH", "nominalBatteryCapacity": 200}, {"unit": "V", "systemVoltageSetting": 255}, {"unit": "V", "recognizedVoltage": 2}, {"unit": "string", "batteryType": "sealed"}, {"unit": "V", "overVoltageThreshold": 160}, {"unit": "V", "chargingVoltageLimit": 155}, {"unit": "V", "equalizingChargingVoltage": 146}, {"unit": "V", "boostchargingVoltage": 144}, {"unit": "V", "floatingChargingVoltage": 138}], "lightControl": {"common": [{"unit": "minute", "lightControlDelay": 5}, {"unit": "V", "lightControlVoltage": 5}], "specialPowerControl": [{"unit": "V", "eachNightOnFunctionEnabled": true}, {"unit": "V", "specialPowerControlFunctionEnabled": false}, {"unit": "V", "noChargingBelowZero": false}, {"unit": "V", "charging method": "direct charging"}]}}	2
2025-09-08 16:02:40.408629	{"ts": 1757336557.4172957, "common": [{"unit": "V", "boostchargingRecoveryVoltage": 132}, {"unit": "V", "overDischargeRecoveryVoltage": 126}, {"unit": "V", "underVoltageWarningLevel": 120}, {"unit": "V", "overDischargeVoltage": 111}, {"unit": "V", "dischargingLimitVoltage": 106}, {"unit": "second", "overDischareTimeDelay": 5}, {"unit": "minute", "equalizingChargingTime": 120}, {"unit": "minute", "boostChargingTime": 120}, {"unit": "day", "equalizingChargingInterval": 30}, {"unit": "mV", "temperatureCompensationFactor": 3}, {"unit": "string", "loadWorkingMode": "Manual mode"}], "battery": [{"unit": "AH", "nominalBatteryCapacity": 200}, {"unit": "V", "systemVoltageSetting": 255}, {"unit": "V", "recognizedVoltage": 2}, {"unit": "string", "batteryType": "sealed"}, {"unit": "V", "overVoltageThreshold": 160}, {"unit": "V", "chargingVoltageLimit": 155}, {"unit": "V", "equalizingChargingVoltage": 146}, {"unit": "V", "boostchargingVoltage": 144}, {"unit": "V", "floatingChargingVoltage": 138}], "lightControl": {"common": [{"unit": "minute", "lightControlDelay": 5}, {"unit": "V", "lightControlVoltage": 5}], "specialPowerControl": [{"unit": "V", "eachNightOnFunctionEnabled": true}, {"unit": "V", "specialPowerControlFunctionEnabled": false}, {"unit": "V", "noChargingBelowZero": false}, {"unit": "V", "charging method": "direct charging"}]}}	2
2025-09-08 18:00:58.745514	{"ts": 1757343655.7534318, "common": [{"unit": "V", "boostchargingRecoveryVoltage": 132}, {"unit": "V", "overDischargeRecoveryVoltage": 126}, {"unit": "V", "underVoltageWarningLevel": 120}, {"unit": "V", "overDischargeVoltage": 111}, {"unit": "V", "dischargingLimitVoltage": 106}, {"unit": "second", "overDischareTimeDelay": 5}, {"unit": "minute", "equalizingChargingTime": 120}, {"unit": "minute", "boostChargingTime": 120}, {"unit": "day", "equalizingChargingInterval": 30}, {"unit": "mV", "temperatureCompensationFactor": 3}, {"unit": "string", "loadWorkingMode": "Manual mode"}], "battery": [{"unit": "AH", "nominalBatteryCapacity": 200}, {"unit": "V", "systemVoltageSetting": 255}, {"unit": "V", "recognizedVoltage": 2}, {"unit": "string", "batteryType": "sealed"}, {"unit": "V", "overVoltageThreshold": 160}, {"unit": "V", "chargingVoltageLimit": 155}, {"unit": "V", "equalizingChargingVoltage": 146}, {"unit": "V", "boostchargingVoltage": 144}, {"unit": "V", "floatingChargingVoltage": 138}], "lightControl": {"common": [{"unit": "minute", "lightControlDelay": 5}, {"unit": "V", "lightControlVoltage": 5}], "specialPowerControl": [{"unit": "V", "eachNightOnFunctionEnabled": true}, {"unit": "V", "specialPowerControlFunctionEnabled": false}, {"unit": "V", "noChargingBelowZero": false}, {"unit": "V", "charging method": "direct charging"}]}}	2
2025-09-08 18:07:19.484248	{"ts": 1757344036.48961, "common": [{"unit": "V", "boostchargingRecoveryVoltage": 132}, {"unit": "V", "overDischargeRecoveryVoltage": 126}, {"unit": "V", "underVoltageWarningLevel": 120}, {"unit": "V", "overDischargeVoltage": 111}, {"unit": "V", "dischargingLimitVoltage": 106}, {"unit": "second", "overDischareTimeDelay": 5}, {"unit": "minute", "equalizingChargingTime": 120}, {"unit": "minute", "boostChargingTime": 120}, {"unit": "day", "equalizingChargingInterval": 30}, {"unit": "mV", "temperatureCompensationFactor": 3}, {"unit": "string", "loadWorkingMode": "Manual mode"}], "battery": [{"unit": "AH", "nominalBatteryCapacity": 200}, {"unit": "V", "systemVoltageSetting": 255}, {"unit": "V", "recognizedVoltage": 2}, {"unit": "string", "batteryType": "sealed"}, {"unit": "V", "overVoltageThreshold": 160}, {"unit": "V", "chargingVoltageLimit": 155}, {"unit": "V", "equalizingChargingVoltage": 146}, {"unit": "V", "boostchargingVoltage": 144}, {"unit": "V", "floatingChargingVoltage": 138}], "lightControl": {"common": [{"unit": "minute", "lightControlDelay": 5}, {"unit": "V", "lightControlVoltage": 5}], "specialPowerControl": [{"unit": "V", "eachNightOnFunctionEnabled": true}, {"unit": "V", "specialPowerControlFunctionEnabled": false}, {"unit": "V", "noChargingBelowZero": false}, {"unit": "V", "charging method": "direct charging"}]}}	2
2025-09-09 08:10:50.2316	{"ts": 1757394647.179449, "common": [{"unit": "V", "boostchargingRecoveryVoltage": 132}, {"unit": "V", "overDischargeRecoveryVoltage": 126}, {"unit": "V", "underVoltageWarningLevel": 120}, {"unit": "V", "overDischargeVoltage": 111}, {"unit": "V", "dischargingLimitVoltage": 106}, {"unit": "second", "overDischareTimeDelay": 5}, {"unit": "minute", "equalizingChargingTime": 120}, {"unit": "minute", "boostChargingTime": 120}, {"unit": "day", "equalizingChargingInterval": 30}, {"unit": "mV", "temperatureCompensationFactor": 3}, {"unit": "string", "loadWorkingMode": "Manual mode"}], "battery": [{"unit": "AH", "nominalBatteryCapacity": 200}, {"unit": "V", "systemVoltageSetting": 255}, {"unit": "V", "recognizedVoltage": 2}, {"unit": "string", "batteryType": "sealed"}, {"unit": "V", "overVoltageThreshold": 160}, {"unit": "V", "chargingVoltageLimit": 155}, {"unit": "V", "equalizingChargingVoltage": 146}, {"unit": "V", "boostchargingVoltage": 144}, {"unit": "V", "floatingChargingVoltage": 138}], "lightControl": {"common": [{"unit": "minute", "lightControlDelay": 5}, {"unit": "V", "lightControlVoltage": 5}], "specialPowerControl": [{"unit": "V", "eachNightOnFunctionEnabled": true}, {"unit": "V", "specialPowerControlFunctionEnabled": false}, {"unit": "V", "noChargingBelowZero": false}, {"unit": "V", "charging method": "direct charging"}]}}	2
2025-09-09 08:23:30.393399	{"ts": 1757395407.3403292, "battery": {"batteryType": "sealed", "recognizedVoltage": 2, "boostchargingVoltage": 144, "chargingVoltageLimit": 155, "overVoltageThreshold": 160, "systemVoltageSetting": 255, "nominalBatteryCapacity": 200, "floatingChargingVoltage": 138, "equalizingChargingVoltage": 146}, "lightControl": {"lightControlDelay": 5, "lightControlVoltage": 5, "specialPowerControl": [{"unit": "V", "eachNightOnFunctionEnabled": true}, {"unit": "V", "specialPowerControlFunctionEnabled": false}, {"unit": "V", "noChargingBelowZero": false}, {"unit": "V", "charging method": "direct charging"}]}, "loadWorkingMode": "Manual mode", "boostChargingTime": 120, "overDischargeVoltage": 111, "overDischareTimeDelay": 5, "equalizingChargingTime": 120, "dischargingLimitVoltage": 106, "underVoltageWarningLevel": 120, "equalizingChargingInterval": 30, "boostchargingRecoveryVoltage": 132, "overDischargeRecoveryVoltage": 126, "temperatureCompensationFactor": 3}	2
2025-09-09 08:35:19.32372	{"ts": 1757396116.2697105, "battery": {"batteryType": "sealed", "recognizedVoltage": 2, "boostchargingVoltage": 144, "chargingVoltageLimit": 155, "overVoltageThreshold": 160, "systemVoltageSetting": 255, "nominalBatteryCapacity": 200, "floatingChargingVoltage": 138, "equalizingChargingVoltage": 146}, "lightControl": {"lightControlDelay": 5, "lightControlVoltage": 5, "specialPowerControl": {"chargingMethod": "direct charging", "noChargingBelowZero": false, "eachNightOnFunctionEnabled": true, "specialPowerControlFunctionEnabled": false}}, "loadWorkingMode": "Manual mode", "boostChargingTime": 120, "overDischargeVoltage": 111, "overDischareTimeDelay": 5, "equalizingChargingTime": 120, "dischargingLimitVoltage": 106, "underVoltageWarningLevel": 120, "equalizingChargingInterval": 30, "boostchargingRecoveryVoltage": 132, "overDischargeRecoveryVoltage": 126, "temperatureCompensationFactor": 3}	2
2025-09-09 09:12:30.58659	{"ts": 1757398347.5326986, "battery": {"batteryType": "sealed", "recognizedVoltage": 2, "boostchargingVoltage": 144, "chargingVoltageLimit": 155, "overVoltageThreshold": 160, "systemVoltageSetting": 255, "nominalBatteryCapacity": 200, "floatingChargingVoltage": 138, "equalizingChargingVoltage": 146}, "lightControl": {"lightControlDelay": 5, "lightControlVoltage": 5, "specialPowerControl": {"chargingMethod": "direct charging", "noChargingBelowZero": false, "eachNightOnFunctionEnabled": true, "specialPowerControlFunctionEnabled": false}}, "loadWorkingMode": "Manual mode", "boostChargingTime": 120, "overDischargeVoltage": 111, "overDischareTimeDelay": 5, "equalizingChargingTime": 120, "dischargingLimitVoltage": 106, "underVoltageWarningLevel": 120, "equalizingChargingInterval": 30, "boostchargingRecoveryVoltage": 132, "overDischargeRecoveryVoltage": 126, "temperatureCompensationFactor": 3}	2
\.


--
-- Data for Name: event_log; Type: TABLE DATA; Schema: device; Owner: postgres
--

COPY device.event_log (id, event_type, event_name, description, created_at, device_id, severity, metadata) FROM stdin;
249	EVENT	login	вход пользователя user	2025-09-08 18:32:08.291086	\N	INFO	\N
250	EVENT	login	вход пользователя user	2025-09-08 18:34:47.166847	\N	INFO	\N
251	EVENT	login	вход пользователя user	2025-09-08 18:37:26.263594	\N	INFO	\N
252	EVENT	login	вход пользователя user	2025-09-08 18:44:15.615297	\N	INFO	\N
253	EVENT	login	вход пользователя user	2025-09-08 18:46:48.52848	\N	INFO	\N
254	EVENT	login	вход пользователя user	2025-09-09 07:47:19.07508	\N	INFO	\N
255	EVENT	login	вход пользователя user	2025-09-09 07:48:02.134882	\N	INFO	\N
256	EVENT	login	вход пользователя user	2025-09-09 07:51:22.599248	\N	INFO	\N
257	EVENT	login	вход пользователя user	2025-09-09 07:53:27.810688	\N	INFO	\N
258	EVENT	login	вход пользователя user	2025-09-09 07:56:53.5037	\N	INFO	\N
259	EVENT	login	вход пользователя user	2025-09-09 08:00:12.156318	\N	INFO	\N
260	EVENT	login	вход пользователя user	2025-09-09 08:11:04.074195	\N	INFO	\N
261	EVENT	login	вход пользователя user	2025-09-09 09:16:56.455073	\N	INFO	\N
262	EVENT	login	вход пользователя user	2025-09-09 09:17:54.945673	\N	INFO	\N
263	EVENT	login	вход пользователя user	2025-09-09 09:18:25.074621	\N	INFO	\N
264	EVENT	login	вход пользователя user	2025-09-09 09:23:48.887545	\N	INFO	\N
265	EVENT	login	вход пользователя user	2025-09-09 09:24:29.949805	\N	INFO	\N
266	EVENT	login	вход пользователя user	2025-09-09 09:25:10.390798	\N	INFO	\N
267	EVENT	login	вход пользователя user	2025-09-09 09:25:34.491941	\N	INFO	\N
268	EVENT	login	вход пользователя user	2025-09-09 09:25:59.423759	\N	INFO	\N
269	EVENT	login	вход пользователя user	2025-09-09 09:26:15.6792	\N	INFO	\N
270	EVENT	login	вход пользователя user	2025-09-09 09:26:39.075713	\N	INFO	\N
271	EVENT	login	вход пользователя user	2025-09-09 09:27:38.19869	\N	INFO	\N
272	EVENT	login	вход пользователя user	2025-09-09 09:27:56.010213	\N	INFO	\N
273	EVENT	login	вход пользователя user	2025-09-09 09:28:19.644144	\N	INFO	\N
274	EVENT	login	вход пользователя user	2025-09-09 09:28:30.481168	\N	INFO	\N
275	EVENT	login	вход пользователя user	2025-09-09 09:29:52.830922	\N	INFO	\N
276	EVENT	login	вход пользователя user	2025-09-09 09:38:41.427986	\N	INFO	\N
\.


--
-- Data for Name: history; Type: TABLE DATA; Schema: device; Owner: postgres
--

COPY device.history (created_at, day, payload, device_id, actual_date) FROM stdin;
\.


--
-- Data for Name: system_information; Type: TABLE DATA; Schema: device; Owner: postgres
--

COPY device.system_information (device_id, payload, created_at) FROM stdin;
2	[{"unit": "V", "maxSupportVoltage": 24}, {"unit": "A", "retedChargingCurrent": 20}, {"unit": "A", "ratedDischargeCurrent": 20}, {"unit": "string", "deviceType": "controller"}, {"unit": "string", "model": "    ML2420      "}, {"unit": "string", "softwareVersion": "0.4.4.2"}, {"unit": "string", "hardwareVersion": "2.0.0.3"}, {"unit": "string", "serialNumber": "0710100"}]	2025-09-08 18:16:08.286668
2	[{"unit": "V", "maxSupportVoltage": 24}, {"unit": "A", "retedChargingCurrent": 20}, {"unit": "A", "ratedDischargeCurrent": 20}, {"unit": "string", "deviceType": "controller"}, {"unit": "string", "model": "    ML2420      "}, {"unit": "string", "softwareVersion": "0.4.4.2"}, {"unit": "string", "hardwareVersion": "2.0.0.3"}, {"unit": "string", "serialNumber": "0710100"}]	2025-09-09 08:06:41.12133
2	[{"unit": "V", "maxSupportVoltage": 24}, {"unit": "A", "retedChargingCurrent": 20}, {"unit": "A", "ratedDischargeCurrent": 20}, {"unit": "string", "deviceType": "controller"}, {"unit": "string", "model": "    ML2420      "}, {"unit": "string", "softwareVersion": "0.4.4.2"}, {"unit": "string", "hardwareVersion": "2.0.0.3"}, {"unit": "string", "serialNumber": "0710100"}]	2025-09-09 08:07:57.798804
2	[{"unit": "V", "maxSupportVoltage": 24}, {"unit": "A", "retedChargingCurrent": 20}, {"unit": "A", "ratedDischargeCurrent": 20}, {"unit": "string", "deviceType": "controller"}, {"unit": "string", "model": "    ML2420      "}, {"unit": "string", "softwareVersion": "0.4.4.2"}, {"unit": "string", "hardwareVersion": "2.0.0.3"}, {"unit": "string", "serialNumber": "0710100"}]	2025-09-09 08:09:43.48833
2	[{"unit": "V", "maxSupportVoltage": 24}, {"unit": "A", "retedChargingCurrent": 20}, {"unit": "A", "ratedDischargeCurrent": 20}, {"unit": "string", "deviceType": "controller"}, {"unit": "string", "model": "    ML2420      "}, {"unit": "string", "softwareVersion": "0.4.4.2"}, {"unit": "string", "hardwareVersion": "2.0.0.3"}, {"unit": "string", "serialNumber": "0710100"}]	2025-09-09 08:10:44.510695
2	[{"unit": "V", "maxSupportVoltage": 24}, {"unit": "A", "retedChargingCurrent": 20}, {"unit": "A", "ratedDischargeCurrent": 20}, {"unit": "string", "deviceType": "controller"}, {"unit": "string", "model": "    ML2420      "}, {"unit": "string", "softwareVersion": "0.4.4.2"}, {"unit": "string", "hardwareVersion": "2.0.0.3"}, {"unit": "string", "serialNumber": "0710100"}]	2025-09-09 08:23:24.654787
2	[{"unit": "V", "maxSupportVoltage": 24}, {"unit": "A", "retedChargingCurrent": 20}, {"unit": "A", "ratedDischargeCurrent": 20}, {"unit": "string", "deviceType": "controller"}, {"unit": "string", "model": "    ML2420      "}, {"unit": "string", "softwareVersion": "0.4.4.2"}, {"unit": "string", "hardwareVersion": "2.0.0.3"}, {"unit": "string", "serialNumber": "0710100"}]	2025-09-09 08:35:13.584042
2	[{"unit": "V", "maxSupportVoltage": 24}, {"unit": "A", "retedChargingCurrent": 20}, {"unit": "A", "ratedDischargeCurrent": 20}, {"unit": "string", "deviceType": "controller"}, {"unit": "string", "model": "    ML2420      "}, {"unit": "string", "softwareVersion": "0.4.4.2"}, {"unit": "string", "hardwareVersion": "2.0.0.3"}, {"unit": "string", "serialNumber": "0710100"}]	2025-09-09 09:12:24.851948
\.


--
-- Data for Name: complex_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.complex_settings (id, param, value, created_at) FROM stdin;
\.


--
-- Name: command_history_id_seq; Type: SEQUENCE SET; Schema: device; Owner: postgres
--

SELECT pg_catalog.setval('device.command_history_id_seq', 13392, true);


--
-- Name: complex_settings_id_seq; Type: SEQUENCE SET; Schema: device; Owner: postgres
--

SELECT pg_catalog.setval('device.complex_settings_id_seq', 15, true);


--
-- Name: dynamic_information_id_seq; Type: SEQUENCE SET; Schema: device; Owner: postgres
--

SELECT pg_catalog.setval('device.dynamic_information_id_seq', 512627, true);


--
-- Name: event_log_id_seq; Type: SEQUENCE SET; Schema: device; Owner: postgres
--

SELECT pg_catalog.setval('device.event_log_id_seq', 276, true);


--
-- Name: complex_settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.complex_settings_id_seq', 1, false);


--
-- Name: command_history command_history_pk; Type: CONSTRAINT; Schema: device; Owner: postgres
--

ALTER TABLE ONLY device.command_history
    ADD CONSTRAINT command_history_pk PRIMARY KEY (id);


--
-- Name: complex_settings complex_settings_param_key; Type: CONSTRAINT; Schema: device; Owner: postgres
--

ALTER TABLE ONLY device.complex_settings
    ADD CONSTRAINT complex_settings_param_key UNIQUE (param);


--
-- Name: complex_settings complex_settings_pkey; Type: CONSTRAINT; Schema: device; Owner: postgres
--

ALTER TABLE ONLY device.complex_settings
    ADD CONSTRAINT complex_settings_pkey PRIMARY KEY (id);


--
-- Name: dynamic_information dynamic_information_pk; Type: CONSTRAINT; Schema: device; Owner: postgres
--

ALTER TABLE ONLY device.dynamic_information
    ADD CONSTRAINT dynamic_information_pk PRIMARY KEY (id);


--
-- Name: event_log event_log_pk; Type: CONSTRAINT; Schema: device; Owner: postgres
--

ALTER TABLE ONLY device.event_log
    ADD CONSTRAINT event_log_pk PRIMARY KEY (id);


--
-- Name: complex_settings complex_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.complex_settings
    ADD CONSTRAINT complex_settings_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

