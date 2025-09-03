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
    options jsonb
);


ALTER TABLE device.complex_settings OWNER TO postgres;

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
-- Name: system_information; Type: TABLE; Schema: device; Owner: postgres
--

CREATE TABLE device.system_information (
    device_id integer NOT NULL,
    payload jsonb NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE device.system_information OWNER TO postgres;

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

COPY device.complex_settings (id, param, value, created_at, descr, type, options) FROM stdin;
1	version	1.0.1	2025-08-25 09:37:37.974177	Версия АК	string	\N
2	coordinates	55.7558, 37.6173	2025-08-25 09:37:37.974177	местоположение	string	\N
3	battery_type	свинцово-кислотный	2025-08-25 09:37:37.974177	тип батареи	select	["ВРЛА", "гелий", "свинцово-кислотный", "литиевый"]
4	params_log_period	300	2025-08-25 09:37:37.974177	Частота записы в журнал параметров работы	string	\N
7	time_source	NTP	2025-08-26 14:49:28.06652	источник точного времени тип	select	["NTP", "RTC"]
8	time_source_addr	pool.ntp.org	2025-08-26 14:49:28.06652	адрес источника точного времени	string	\N
9	its_connection_period	60	2025-08-26 14:49:28.06652	Пероид выхода на связь с ИТС:	string	\N
11	switch_off_modem	false	2025-08-26 14:49:28.06652	Отключать модем после сеанса связи	boolean	\N
12	modem_off_delay	10	2025-08-26 14:49:28.06652	Время удержания модема после связи минут	string	\N
5	load_work_mode	откл.	2025-08-26 14:49:28.06652	Режим работы светильника	select	["режим", "откл.", "вкл."]
10	keep_connection_alive	true	2025-08-26 14:49:28.06652	Режим постоянной связи: (да / нет)	boolean	\N
6	trafficlight_work_mode	режим 3 (алгоритм)	2025-08-26 14:49:28.06652	Режим работы светофора	select	["режим 1 (1Гц, 500мс)", "режим 2 (1Гц, 100мс)", "режим 3 (алгоритм)", "режим 4 (откл.)"]
\.


--
-- Data for Name: dynamic_information; Type: TABLE DATA; Schema: device; Owner: postgres
--

COPY device.dynamic_information (id, created_at, payload, device_id) FROM stdin;
476982	2025-09-03 20:34:50.525775	{"ts": 1756920887.3450942, "load": {"amps": 0.0, "state": false, "volts": 0.0, "watts": 0, "maxAmps": 0.43, "maxWatts": 5, "dailyPower": 0.0, "totalPower": "0.0", "dailyAmpHours": 0, "totalAmpHours": 0.0}, "faults": [], "panels": {"amps": 0.0, "volts": 18.8}, "battery": {"volts": 13.8, "maxVolts": 14.4, "minVolts": 0.0, "temperature": 23, "stateOfCharge": 100}, "charging": {"amps": 0.0, "watts": 0, "maxAmps": 0.89, "maxWatts": 12, "dailyPower": 0.0, "totalPower": 0.027, "dailyAmpHours": 0, "totalAmpHours": 0.002}, "controller": {"days": 8, "fullCharges": 2, "temperature": 24, "chargingMode": "FLOAT", "overDischarges": 5}, "modbusError": false}	0
\.


--
-- Data for Name: eeprom_parameter_setting; Type: TABLE DATA; Schema: device; Owner: postgres
--

COPY device.eeprom_parameter_setting (created_at, payload, device_id) FROM stdin;
2025-05-23 16:24:18.036916	{"battery": {"batteryType": "sealed", "recognizedVoltage": 12, "boostchargingVoltage": 144, "chargingVoltageLimit": 155, "overVoltageThreshold": 160, "systemVoltageSetting": 255, "nominalBatteryCapacity": 200, "floatingChargingVoltage": 138, "equalizingChargingVoltage": 146}, "lightControl": {"lightControlDelay": 5, "lightControlVoltage": 5, "specialPowerControl": {"charging method": "direct charging", "noChargingBelowZero": false, "eachNightOnFunctionEnabled": true, "specialPowerControlFunctionEnabled": false}}, "loadWorkingMode": "Manual mode", "boostChargingTime": 120, "overDischargeVoltage": 111, "overDischareTimeDelay": 5, "equalizingChargingTime": 120, "dischargingLimitVoltage": 106, "underVoltageWarningLevel": 120, "boostchargingRecoveryVoltage": 132, "equalizing charging interval": 30, "overDischargeRecoveryVoltage": 126, "temperatureCompensationFactor": 3}	2
\.


--
-- Data for Name: event_log; Type: TABLE DATA; Schema: device; Owner: postgres
--

COPY device.event_log (id, event_type, event_name, description, created_at, device_id, severity, metadata) FROM stdin;
1	EVENT	login	вход пользователя	2025-08-27 14:53:42.292469	\N	INFO	\N
2	EVENT	login	user	2025-08-27 14:56:45.265645	\N	INFO	\N
3	EVENT	login	user	2025-08-27 15:05:01.985266	\N	INFO	\N
4	EVENT	login	user	2025-08-27 15:14:29.910074	\N	INFO	\N
5	EVENT	login	user	2025-08-27 15:18:02.181952	\N	INFO	\N
6	EVENT	login	вход пользователя user	2025-08-27 15:20:31.79183	\N	INFO	\N
7	EVENT	login	вход пользователя user	2025-08-27 16:22:03.199964	\N	INFO	\N
8	EVENT	login	вход пользователя user	2025-08-27 16:34:40.424453	\N	INFO	\N
9	EVENT	login	вход пользователя user	2025-08-27 16:35:44.999815	\N	INFO	\N
10	EVENT	login	вход пользователя user	2025-08-27 22:32:15.333747	\N	INFO	\N
11	EVENT	login	вход пользователя user	2025-08-30 16:20:43.383248	\N	INFO	\N
12	EVENT	login	вход пользователя user	2025-08-30 16:23:36.560279	\N	INFO	\N
13	EVENT	login	вход пользователя user	2025-08-30 16:24:51.828145	\N	INFO	\N
14	EVENT	login	вход пользователя user	2025-08-30 16:28:31.34176	\N	INFO	\N
15	EVENT	login	вход пользователя user	2025-08-30 16:29:29.812181	\N	INFO	\N
16	EVENT	login	вход пользователя user	2025-08-30 16:30:54.89195	\N	INFO	\N
17	EVENT	login	вход пользователя user	2025-08-30 16:32:28.85674	\N	INFO	\N
18	EVENT	login	вход пользователя user	2025-08-30 16:32:55.060746	\N	INFO	\N
19	EVENT	login	вход пользователя user	2025-08-30 16:40:00.742599	\N	INFO	\N
20	EVENT	login	вход пользователя user	2025-08-30 16:40:14.862597	\N	INFO	\N
21	EVENT	login	вход пользователя user	2025-08-30 16:41:45.380661	\N	INFO	\N
22	EVENT	login	вход пользователя user	2025-08-30 16:42:07.599174	\N	INFO	\N
23	EVENT	login	вход пользователя user	2025-09-01 16:37:29.596324	\N	INFO	\N
24	EVENT	login	вход пользователя user	2025-09-01 16:37:47.010108	\N	INFO	\N
25	EVENT	login	вход пользователя user	2025-09-01 16:37:56.692772	\N	INFO	\N
26	EVENT	login	вход пользователя user	2025-09-01 16:40:11.809094	\N	INFO	\N
27	EVENT	login	вход пользователя user	2025-09-01 16:46:20.007389	\N	INFO	\N
28	EVENT	login	вход пользователя user	2025-09-01 16:47:24.628935	\N	INFO	\N
29	EVENT	login	вход пользователя user	2025-09-01 16:48:42.072963	\N	INFO	\N
30	EVENT	login	вход пользователя user	2025-09-01 16:50:05.527088	\N	INFO	\N
31	EVENT	login	вход пользователя user	2025-09-01 16:57:01.834699	\N	INFO	\N
32	EVENT	login	вход пользователя user	2025-09-01 18:32:23.780759	\N	INFO	\N
33	EVENT	login	вход пользователя user	2025-09-01 18:35:48.552566	\N	INFO	\N
34	EVENT	login	вход пользователя user	2025-09-01 18:38:13.161268	\N	INFO	\N
35	EVENT	login	вход пользователя user	2025-09-01 19:17:11.528967	\N	INFO	\N
36	EVENT	login	вход пользователя user	2025-09-01 19:17:23.882232	\N	INFO	\N
37	EVENT	login	вход пользователя user	2025-09-01 19:20:19.625578	\N	INFO	\N
38	EVENT	login	вход пользователя user	2025-09-01 19:21:04.228712	\N	INFO	\N
39	EVENT	login	вход пользователя user	2025-09-01 19:21:18.372756	\N	INFO	\N
40	EVENT	login	вход пользователя user	2025-09-02 10:15:23.736405	\N	INFO	\N
41	EVENT	login	вход пользователя user	2025-09-02 10:25:17.538444	\N	INFO	\N
42	EVENT	wifi	off	2025-09-02 10:25:20.548068	\N	INFO	\N
43	EVENT	wifi	on	2025-09-02 10:25:22.483788	\N	INFO	\N
44	EVENT	wifi	off	2025-09-02 10:25:44.216751	\N	INFO	\N
45	EVENT	wifi	on	2025-09-02 10:25:46.316638	\N	INFO	\N
46	EVENT	login	вход пользователя user	2025-09-02 11:00:14.968782	\N	INFO	\N
47	EVENT	wifi	on	2025-09-02 11:00:27.040033	\N	INFO	\N
48	EVENT	login	вход пользователя user	2025-09-02 11:31:13.448916	\N	INFO	\N
49	EVENT	wifi	on	2025-09-02 11:44:38.130161	\N	INFO	\N
50	EVENT	wifi	on	2025-09-02 11:54:45.534638	\N	INFO	\N
51	EVENT	wifi	off	2025-09-02 11:55:11.390527	\N	INFO	\N
52	EVENT	wifi	on	2025-09-02 11:55:29.952017	\N	INFO	\N
53	EVENT	login	вход пользователя user	2025-09-02 13:37:33.745229	\N	INFO	\N
54	EVENT	wifi	on	2025-09-02 13:37:36.442988	\N	INFO	\N
55	EVENT	wifi	off	2025-09-02 13:37:48.608992	\N	INFO	\N
56	EVENT	login	вход пользователя user	2025-09-02 14:44:44.029072	\N	INFO	\N
57	EVENT	wifi	on	2025-09-02 14:44:44.210826	\N	INFO	\N
58	EVENT	wifi	off	2025-09-02 14:44:44.21715	\N	INFO	\N
59	EVENT	wifi	on	2025-09-02 14:44:44.292998	\N	INFO	\N
60	EVENT	wifi	off	2025-09-02 14:44:44.308326	\N	INFO	\N
61	EVENT	wifi	on	2025-09-02 14:44:44.373805	\N	INFO	\N
62	EVENT	wifi	off	2025-09-02 14:44:44.394633	\N	INFO	\N
63	EVENT	wifi	on	2025-09-02 14:44:44.452206	\N	INFO	\N
64	EVENT	wifi	off	2025-09-02 14:44:44.474852	\N	INFO	\N
65	EVENT	wifi	on	2025-09-02 14:44:49.171789	\N	INFO	\N
66	EVENT	wifi	off	2025-09-02 14:44:49.177212	\N	INFO	\N
67	EVENT	wifi	on	2025-09-02 14:44:49.265457	\N	INFO	\N
68	EVENT	wifi	off	2025-09-02 14:44:49.282056	\N	INFO	\N
69	EVENT	wifi	on	2025-09-02 14:44:49.361033	\N	INFO	\N
70	EVENT	wifi	off	2025-09-02 14:44:49.370872	\N	INFO	\N
71	EVENT	wifi	on	2025-09-02 14:44:49.447054	\N	INFO	\N
72	EVENT	wifi	off	2025-09-02 14:44:49.459684	\N	INFO	\N
73	EVENT	wifi	on	2025-09-02 14:44:54.194488	\N	INFO	\N
74	EVENT	wifi	off	2025-09-02 14:44:54.199445	\N	INFO	\N
75	EVENT	wifi	on	2025-09-02 14:44:54.270428	\N	INFO	\N
76	EVENT	wifi	off	2025-09-02 14:44:54.293771	\N	INFO	\N
77	EVENT	wifi	on	2025-09-02 14:44:54.394549	\N	INFO	\N
78	EVENT	wifi	off	2025-09-02 14:44:54.406407	\N	INFO	\N
79	EVENT	wifi	on	2025-09-02 14:44:54.468778	\N	INFO	\N
80	EVENT	wifi	off	2025-09-02 14:44:54.487645	\N	INFO	\N
81	EVENT	wifi	on	2025-09-02 14:44:59.208601	\N	INFO	\N
82	EVENT	wifi	off	2025-09-02 14:44:59.213281	\N	INFO	\N
83	EVENT	wifi	on	2025-09-02 14:44:59.2929	\N	INFO	\N
84	EVENT	wifi	off	2025-09-02 14:44:59.306472	\N	INFO	\N
85	EVENT	wifi	on	2025-09-02 14:44:59.438515	\N	INFO	\N
86	EVENT	wifi	off	2025-09-02 14:44:59.444784	\N	INFO	\N
87	EVENT	wifi	on	2025-09-02 14:44:59.517861	\N	INFO	\N
88	EVENT	wifi	off	2025-09-02 14:44:59.532905	\N	INFO	\N
89	EVENT	wifi	on	2025-09-02 14:45:04.23184	\N	INFO	\N
90	EVENT	wifi	off	2025-09-02 14:45:04.235252	\N	INFO	\N
91	EVENT	wifi	on	2025-09-02 14:45:04.307152	\N	INFO	\N
92	EVENT	wifi	off	2025-09-02 14:45:04.322023	\N	INFO	\N
93	EVENT	wifi	off	2025-09-02 14:45:04.445194	\N	INFO	\N
94	EVENT	wifi	on	2025-09-02 14:45:04.46354	\N	INFO	\N
95	EVENT	wifi	off	2025-09-02 14:45:04.523309	\N	INFO	\N
96	EVENT	wifi	on	2025-09-02 14:45:04.545222	\N	INFO	\N
97	EVENT	wifi	on	2025-09-02 14:45:09.255542	\N	INFO	\N
98	EVENT	wifi	off	2025-09-02 14:45:09.282402	\N	INFO	\N
99	EVENT	wifi	on	2025-09-02 14:45:09.336973	\N	INFO	\N
100	EVENT	wifi	off	2025-09-02 14:45:09.35929	\N	INFO	\N
101	EVENT	wifi	off	2025-09-02 14:45:09.48357	\N	INFO	\N
102	EVENT	wifi	on	2025-09-02 14:45:09.50011	\N	INFO	\N
103	EVENT	wifi	off	2025-09-02 14:45:09.560288	\N	INFO	\N
104	EVENT	wifi	on	2025-09-02 14:45:09.581476	\N	INFO	\N
105	EVENT	wifi	on	2025-09-02 14:45:14.259664	\N	INFO	\N
106	EVENT	wifi	off	2025-09-02 14:45:14.265165	\N	INFO	\N
107	EVENT	wifi	on	2025-09-02 14:45:14.333662	\N	INFO	\N
108	EVENT	wifi	off	2025-09-02 14:45:14.351743	\N	INFO	\N
109	EVENT	login	вход пользователя user	2025-09-02 14:46:36.553108	\N	INFO	\N
110	EVENT	wifi	on	2025-09-02 14:46:36.741323	\N	INFO	\N
111	EVENT	wifi	off	2025-09-02 14:46:36.752322	\N	INFO	\N
112	EVENT	wifi	on	2025-09-02 14:46:36.821472	\N	INFO	\N
113	EVENT	wifi	off	2025-09-02 14:46:36.835092	\N	INFO	\N
114	EVENT	wifi	on	2025-09-02 14:46:36.896532	\N	INFO	\N
115	EVENT	wifi	off	2025-09-02 14:46:36.916021	\N	INFO	\N
116	EVENT	wifi	on	2025-09-02 14:46:36.972972	\N	INFO	\N
117	EVENT	wifi	off	2025-09-02 14:46:36.99503	\N	INFO	\N
118	EVENT	wifi	on	2025-09-02 14:46:41.70326	\N	INFO	\N
119	EVENT	wifi	off	2025-09-02 14:46:41.708636	\N	INFO	\N
120	EVENT	wifi	on	2025-09-02 14:46:41.781528	\N	INFO	\N
121	EVENT	wifi	off	2025-09-02 14:46:41.802095	\N	INFO	\N
122	EVENT	wifi	on	2025-09-02 14:46:41.882749	\N	INFO	\N
123	EVENT	wifi	off	2025-09-02 14:46:41.896236	\N	INFO	\N
124	EVENT	wifi	on	2025-09-02 14:46:41.963959	\N	INFO	\N
125	EVENT	wifi	off	2025-09-02 14:46:41.979439	\N	INFO	\N
126	EVENT	wifi	on	2025-09-02 14:46:46.724508	\N	INFO	\N
127	EVENT	wifi	off	2025-09-02 14:46:46.728751	\N	INFO	\N
128	EVENT	wifi	on	2025-09-02 14:46:46.802318	\N	INFO	\N
129	EVENT	wifi	off	2025-09-02 14:46:46.811765	\N	INFO	\N
130	EVENT	wifi	on	2025-09-02 14:46:46.877235	\N	INFO	\N
131	EVENT	wifi	off	2025-09-02 14:46:46.891688	\N	INFO	\N
132	EVENT	wifi	on	2025-09-02 14:46:46.953156	\N	INFO	\N
133	EVENT	wifi	off	2025-09-02 14:46:46.973087	\N	INFO	\N
134	EVENT	wifi	on	2025-09-02 14:46:51.772506	\N	INFO	\N
135	EVENT	wifi	off	2025-09-02 14:46:51.792577	\N	INFO	\N
136	EVENT	wifi	on	2025-09-02 14:46:51.849957	\N	INFO	\N
137	EVENT	wifi	off	2025-09-02 14:46:51.883209	\N	INFO	\N
138	EVENT	wifi	on	2025-09-02 14:46:51.929122	\N	INFO	\N
139	EVENT	wifi	off	2025-09-02 14:46:51.953578	\N	INFO	\N
140	EVENT	login	вход пользователя user	2025-09-02 14:48:44.349965	\N	INFO	\N
141	EVENT	wifi	on	2025-09-02 14:48:44.536153	\N	INFO	\N
142	EVENT	wifi	off	2025-09-02 14:48:44.55209	\N	INFO	\N
143	EVENT	wifi	on	2025-09-02 14:48:44.621431	\N	INFO	\N
144	EVENT	wifi	off	2025-09-02 14:48:44.642169	\N	INFO	\N
145	EVENT	wifi	on	2025-09-02 14:48:44.695968	\N	INFO	\N
146	EVENT	wifi	off	2025-09-02 14:48:44.718563	\N	INFO	\N
147	EVENT	wifi	on	2025-09-02 14:48:44.778858	\N	INFO	\N
148	EVENT	wifi	off	2025-09-02 14:48:44.797435	\N	INFO	\N
149	EVENT	wifi	on	2025-09-02 14:48:49.504333	\N	INFO	\N
150	EVENT	wifi	off	2025-09-02 14:48:49.50982	\N	INFO	\N
151	EVENT	wifi	on	2025-09-02 14:48:49.58566	\N	INFO	\N
152	EVENT	wifi	off	2025-09-02 14:48:49.611748	\N	INFO	\N
153	EVENT	wifi	on	2025-09-02 14:48:49.683538	\N	INFO	\N
154	EVENT	wifi	off	2025-09-02 14:48:49.698126	\N	INFO	\N
155	EVENT	wifi	on	2025-09-02 14:48:49.76737	\N	INFO	\N
156	EVENT	wifi	off	2025-09-02 14:48:49.781864	\N	INFO	\N
157	EVENT	login	вход пользователя user	2025-09-02 14:50:40.55719	\N	INFO	\N
158	EVENT	login	вход пользователя user	2025-09-02 14:52:44.753086	\N	INFO	\N
159	EVENT	login	вход пользователя user	2025-09-02 15:08:44.820254	\N	INFO	\N
160	EVENT	login	вход пользователя user	2025-09-02 15:10:35.240668	\N	INFO	\N
161	EVENT	login	вход пользователя user	2025-09-02 15:13:31.052151	\N	INFO	\N
162	EVENT	login	вход пользователя user	2025-09-02 15:18:12.576547	\N	INFO	\N
163	EVENT	login	вход пользователя user	2025-09-02 15:19:32.303621	\N	INFO	\N
164	EVENT	login	вход пользователя user	2025-09-02 15:21:45.856852	\N	INFO	\N
165	EVENT	login	вход пользователя user	2025-09-02 15:22:46.524037	\N	INFO	\N
166	EVENT	login	вход пользователя user	2025-09-02 15:23:33.510672	\N	INFO	\N
167	EVENT	login	вход пользователя user	2025-09-02 15:33:29.805795	\N	INFO	\N
168	EVENT	login	вход пользователя user	2025-09-02 16:37:25.41353	\N	INFO	\N
169	EVENT	login	вход пользователя user	2025-09-02 16:39:33.591114	\N	INFO	\N
170	EVENT	login	вход пользователя user	2025-09-02 16:39:48.561668	\N	INFO	\N
171	EVENT	wifi	on	2025-09-02 16:40:28.855988	\N	INFO	\N
172	EVENT	wifi	off	2025-09-02 16:40:34.208332	\N	INFO	\N
173	EVENT	wifi	on	2025-09-02 16:40:41.276779	\N	INFO	\N
174	EVENT	login	вход пользователя user	2025-09-02 16:48:30.224499	\N	INFO	\N
175	EVENT	login	вход пользователя user	2025-09-02 18:19:09.957574	\N	INFO	\N
176	EVENT	login	вход пользователя user	2025-09-02 18:23:50.800109	\N	INFO	\N
177	EVENT	login	вход пользователя user	2025-09-02 18:24:27.800653	\N	INFO	\N
178	EVENT	login	вход пользователя user	2025-09-02 18:25:21.685012	\N	INFO	\N
179	EVENT	login	вход пользователя user	2025-09-03 09:36:08.812195	\N	INFO	\N
180	EVENT	login	вход пользователя user	2025-09-03 09:53:06.153139	\N	INFO	\N
181	EVENT	login	вход пользователя user	2025-09-03 10:32:07.755431	\N	INFO	\N
182	EVENT	wifi	off	2025-09-03 10:35:24.476901	\N	INFO	\N
183	EVENT	login	вход пользователя user	2025-09-03 10:35:40.278814	\N	INFO	\N
184	EVENT	wifi button	on	2025-09-03 10:37:03.468706	\N	INFO	\N
185	EVENT	wifi button	on	2025-09-03 10:37:04.548974	\N	INFO	\N
186	EVENT	wifi	off	2025-09-03 10:37:19.416573	\N	INFO	\N
187	EVENT	wifi button	on	2025-09-03 10:37:30.052586	\N	INFO	\N
188	EVENT	wifi button	on	2025-09-03 10:37:31.129577	\N	INFO	\N
189	EVENT	wifi button	on	2025-09-03 10:53:14.929341	\N	INFO	\N
190	EVENT	wifi button	on	2025-09-03 10:53:16.008655	\N	INFO	\N
191	EVENT	wifi button	on	2025-09-03 10:53:17.102031	\N	INFO	\N
192	EVENT	wifi button	on	2025-09-03 10:53:18.180605	\N	INFO	\N
193	EVENT	wifi button	on	2025-09-03 10:53:19.260621	\N	INFO	\N
194	EVENT	дверь шкафа	Открыта дверь шкафа	2025-09-03 12:58:09.641137	\N	INFO	\N
195	EVENT	дверь шкафа	Открыта дверь шкафа	2025-09-03 12:58:18.293618	\N	INFO	\N
196	EVENT	дверь шкафа	Закрыта дверь шкафа	2025-09-03 12:58:40.742988	\N	INFO	\N
197	EVENT	дверь шкафа	Открыта дверь шкафа	2025-09-03 12:58:47.922218	\N	INFO	\N
198	EVENT	wifi button	on	2025-09-03 12:59:08.321076	\N	INFO	\N
199	EVENT	wifi button	on	2025-09-03 12:59:09.400836	\N	INFO	\N
200	EVENT	wifi button	on	2025-09-03 12:59:10.480699	\N	INFO	\N
201	EVENT	wifi button	on	2025-09-03 12:59:11.559054	\N	INFO	\N
202	EVENT	wifi button	on	2025-09-03 12:59:12.636317	\N	INFO	\N
203	EVENT	login	вход пользователя user	2025-09-03 14:09:10.396952	\N	INFO	\N
204	EVENT	login	вход пользователя user	2025-09-03 14:16:27.872638	\N	INFO	\N
205	EVENT	дверь шкафа	Закрыта дверь шкафа	2025-09-03 14:17:00.253488	\N	INFO	\N
206	EVENT	дверь шкафа	Открыта дверь шкафа	2025-09-03 14:17:05.372854	\N	INFO	\N
207	EVENT	wifi button	on	2025-09-03 14:17:11.163861	\N	INFO	\N
208	EVENT	wifi button	off	2025-09-03 14:17:13.636668	\N	INFO	\N
209	EVENT	login	вход пользователя user	2025-09-03 14:48:31.267219	\N	INFO	\N
210	EVENT	login	вход пользователя user	2025-09-03 15:26:52.231783	\N	INFO	\N
211	EVENT	login	вход пользователя user	2025-09-03 15:36:17.06861	\N	INFO	\N
212	EVENT	login	вход пользователя user	2025-09-03 15:37:06.66866	\N	INFO	\N
213	EVENT	login	вход пользователя user	2025-09-03 15:37:34.952666	\N	INFO	\N
214	EVENT	login	вход пользователя user	2025-09-03 15:37:48.041544	\N	INFO	\N
215	EVENT	login	вход пользователя user	2025-09-03 15:39:34.896239	\N	INFO	\N
216	EVENT	login	вход пользователя user	2025-09-03 15:47:13.975522	\N	INFO	\N
217	EVENT	login	вход пользователя user	2025-09-03 16:48:01.585209	\N	INFO	\N
218	EVENT	login	вход пользователя user	2025-09-03 16:50:24.129368	\N	INFO	\N
\.


--
-- Data for Name: history; Type: TABLE DATA; Schema: device; Owner: postgres
--

COPY device.history (created_at, day, payload, device_id, actual_date) FROM stdin;
2025-09-03 20:34:50.637625	1	{"unit": "AH", "chargingAmpHrs": 2, "powerGeneration": 27, "maxChargingPower": 50, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 144, "maxChargingCurrent": 349, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 98}	2	2025-09-02 20:34:50.637625
2025-09-03 20:34:50.81147	2	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 101, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-09-01 20:34:50.81147
2025-09-03 20:34:50.895697	3	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 121, "maxChargingCurrent": 0, "maxDischargingPower": 5, "maxDischargingCurrent": 45, "currentDayMinBatteryVoltage": 120}	2	2025-08-31 20:34:50.895697
2025-09-03 20:34:50.977523	4	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 109, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 107}	2	2025-08-30 20:34:50.977523
2025-09-03 20:34:51.064656	5	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 113, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 109}	2	2025-08-29 20:34:51.064656
2025-09-03 20:34:51.146988	6	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 113, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 112}	2	2025-08-28 20:34:51.146988
2025-09-03 20:34:51.228531	7	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 113, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 113}	2	2025-08-27 20:34:51.228531
2025-09-03 20:34:51.310939	8	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 114, "maxChargingCurrent": 0, "maxDischargingPower": 5, "maxDischargingCurrent": 51, "currentDayMinBatteryVoltage": 111}	2	2025-08-26 20:34:51.310939
2025-09-03 20:34:51.393805	9	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-25 20:34:51.393805
2025-09-03 20:34:51.485711	10	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-24 20:34:51.485711
2025-09-03 20:34:51.566001	11	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-23 20:34:51.566001
2025-09-03 20:34:51.648854	12	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-22 20:34:51.648854
2025-09-03 20:34:51.730246	13	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-21 20:34:51.730246
2025-09-03 20:34:51.809572	14	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-20 20:34:51.809572
2025-09-03 20:34:51.890645	15	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-19 20:34:51.890645
2025-09-03 20:34:51.971219	16	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-18 20:34:51.971219
2025-09-03 20:34:52.054416	17	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-17 20:34:52.054416
2025-09-03 20:34:52.13321	18	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-16 20:34:52.13321
2025-09-03 20:34:52.21605	19	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-15 20:34:52.21605
2025-09-03 20:34:52.299701	20	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-14 20:34:52.299701
2025-09-03 20:34:52.389132	21	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-13 20:34:52.389132
2025-09-03 20:34:52.467088	22	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-12 20:34:52.467088
2025-09-03 20:34:52.547753	23	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-11 20:34:52.547753
2025-09-03 20:34:52.628978	24	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-10 20:34:52.628978
2025-09-03 20:34:52.71026	25	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-09 20:34:52.71026
2025-09-03 20:34:52.791279	26	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-08 20:34:52.791279
2025-09-03 20:34:52.874154	27	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-07 20:34:52.874154
2025-09-03 20:34:52.957116	28	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-06 20:34:52.957116
2025-09-03 20:34:53.038513	29	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-05 20:34:53.038513
2025-09-03 20:34:53.117438	30	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-04 20:34:53.117438
2025-09-03 20:34:53.199154	31	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-03 20:34:53.199154
2025-09-03 20:34:53.339956	32	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-02 20:34:53.339956
2025-09-03 20:34:53.418797	33	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-08-01 20:34:53.418797
2025-09-03 20:34:53.499423	34	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-31 20:34:53.499423
2025-09-03 20:34:53.580294	35	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-30 20:34:53.580294
2025-09-03 20:34:53.65924	36	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-29 20:34:53.65924
2025-09-03 20:34:53.736304	37	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-28 20:34:53.736304
2025-09-03 20:34:53.813137	38	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-27 20:34:53.813137
2025-09-03 20:34:53.894453	39	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-26 20:34:53.894453
2025-09-03 20:34:53.979766	40	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-25 20:34:53.979766
2025-09-03 20:34:54.061094	41	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-24 20:34:54.061094
2025-09-03 20:34:54.143722	42	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-23 20:34:54.143722
2025-09-03 20:34:54.225258	43	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-22 20:34:54.225258
2025-09-03 20:34:54.307998	44	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-21 20:34:54.307998
2025-09-03 20:34:54.387768	45	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-20 20:34:54.387768
2025-09-03 20:34:54.463327	46	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-19 20:34:54.463327
2025-09-03 20:34:54.544645	47	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-18 20:34:54.544645
2025-09-03 20:34:54.629439	48	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-17 20:34:54.629439
2025-09-03 20:34:54.711442	49	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-16 20:34:54.711442
2025-09-03 20:34:54.792843	50	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-15 20:34:54.792843
2025-09-03 20:34:54.873993	51	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-14 20:34:54.873993
2025-09-03 20:34:54.95627	52	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-13 20:34:54.95627
2025-09-03 20:34:55.039917	53	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-12 20:34:55.039917
2025-09-03 20:34:55.123223	54	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-11 20:34:55.123223
2025-09-03 20:34:55.21298	55	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-10 20:34:55.21298
2025-09-03 20:34:55.303741	56	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-09 20:34:55.303741
2025-09-03 20:34:55.383218	57	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-08 20:34:55.383218
2025-09-03 20:34:55.463967	58	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-07 20:34:55.463967
2025-09-03 20:34:55.539941	59	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-06 20:34:55.539941
2025-09-03 20:34:55.621102	60	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-05 20:34:55.621102
2025-09-03 20:34:55.701481	61	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-04 20:34:55.701481
2025-09-03 20:34:55.782732	62	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-03 20:34:55.782732
2025-09-03 20:34:55.865026	63	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-02 20:34:55.865026
2025-09-03 20:34:55.947125	64	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-07-01 20:34:55.947125
2025-09-03 20:34:56.029642	65	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-30 20:34:56.029642
2025-09-03 20:34:56.111516	66	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-29 20:34:56.111516
2025-09-03 20:34:56.205068	67	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-28 20:34:56.205068
2025-09-03 20:34:56.454609	68	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-27 20:34:56.454609
2025-09-03 20:34:56.535155	69	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-26 20:34:56.535155
2025-09-03 20:34:56.613078	70	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-25 20:34:56.613078
2025-09-03 20:34:56.693067	71	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-24 20:34:56.693067
2025-09-03 20:34:56.77512	72	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-23 20:34:56.77512
2025-09-03 20:34:56.853425	73	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-22 20:34:56.853425
2025-09-03 20:34:56.933972	74	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-21 20:34:56.933972
2025-09-03 20:34:57.014264	75	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-20 20:34:57.014264
2025-09-03 20:34:57.095501	76	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-19 20:34:57.095501
2025-09-03 20:34:57.177783	77	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-18 20:34:57.177783
2025-09-03 20:34:57.268494	78	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-17 20:34:57.268494
2025-09-03 20:34:57.349676	79	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-16 20:34:57.349676
2025-09-03 20:34:57.430252	80	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-15 20:34:57.430252
2025-09-03 20:34:57.508578	81	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-14 20:34:57.508578
2025-09-03 20:34:57.588699	82	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-13 20:34:57.588699
2025-09-03 20:34:57.668046	83	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-12 20:34:57.668046
2025-09-03 20:34:57.746361	84	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-11 20:34:57.746361
2025-09-03 20:34:57.824264	85	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-10 20:34:57.824264
2025-09-03 20:34:57.906319	86	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-09 20:34:57.906319
2025-09-03 20:34:57.987408	87	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-08 20:34:57.987408
2025-09-03 20:34:58.070014	88	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-07 20:34:58.070014
2025-09-03 20:34:58.154025	89	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-06 20:34:58.154025
2025-09-03 20:34:58.233481	90	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-05 20:34:58.233481
2025-09-03 20:34:58.313514	91	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-04 20:34:58.313514
2025-09-03 20:34:58.392222	92	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-03 20:34:58.392222
2025-09-03 20:34:58.471834	93	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-02 20:34:58.471834
2025-09-03 20:34:58.551887	94	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-06-01 20:34:58.551887
2025-09-03 20:34:58.632895	95	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-31 20:34:58.632895
2025-09-03 20:34:58.71407	96	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-30 20:34:58.71407
2025-09-03 20:34:58.795976	97	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-29 20:34:58.795976
2025-09-03 20:34:58.877622	98	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-28 20:34:58.877622
2025-09-03 20:34:58.961458	99	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-27 20:34:58.961458
2025-09-03 20:34:59.044838	100	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-26 20:34:59.044838
2025-09-03 20:34:59.123622	101	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-25 20:34:59.123622
2025-09-03 20:34:59.203532	102	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-24 20:34:59.203532
2025-09-03 20:34:59.286702	103	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-23 20:34:59.286702
2025-09-03 20:34:59.368412	104	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-22 20:34:59.368412
2025-09-03 20:34:59.451397	105	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-21 20:34:59.451397
2025-09-03 20:34:59.531367	106	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-20 20:34:59.531367
2025-09-03 20:34:59.611764	107	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-19 20:34:59.611764
2025-09-03 20:34:59.687917	108	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-18 20:34:59.687917
2025-09-03 20:34:59.76893	109	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-17 20:34:59.76893
2025-09-03 20:34:59.850674	110	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-16 20:34:59.850674
2025-09-03 20:34:59.933347	111	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-15 20:34:59.933347
2025-09-03 20:35:00.015717	112	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-14 20:35:00.015717
2025-09-03 20:35:00.09554	113	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-13 20:35:00.09554
2025-09-03 20:35:00.177634	114	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-12 20:35:00.177634
2025-09-03 20:35:00.258525	115	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-11 20:35:00.258525
2025-09-03 20:35:00.339148	116	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-10 20:35:00.339148
2025-09-03 20:35:00.418978	117	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-09 20:35:00.418978
2025-09-03 20:35:00.495384	118	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-08 20:35:00.495384
2025-09-03 20:35:00.573971	119	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-07 20:35:00.573971
2025-09-03 20:35:00.65544	120	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-06 20:35:00.65544
2025-09-03 20:35:00.738424	121	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-05 20:35:00.738424
2025-09-03 20:35:00.819987	122	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-04 20:35:00.819987
2025-09-03 20:35:00.905053	123	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-03 20:35:00.905053
2025-09-03 20:35:00.985645	124	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-02 20:35:00.985645
2025-09-03 20:35:01.063662	125	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-05-01 20:35:01.063662
2025-09-03 20:35:01.143907	126	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-04-30 20:35:01.143907
2025-09-03 20:35:01.22825	127	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-04-29 20:35:01.22825
2025-09-03 20:35:01.31243	128	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-04-28 20:35:01.31243
2025-09-03 20:35:01.391692	129	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-04-27 20:35:01.391692
2025-09-03 20:35:01.469506	130	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-04-26 20:35:01.469506
2025-09-03 20:35:01.54828	131	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-04-25 20:35:01.54828
2025-09-03 20:35:01.66424	132	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-04-24 20:35:01.66424
2025-09-03 20:35:01.743829	133	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-04-23 20:35:01.743829
2025-09-03 20:35:01.82336	134	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-04-22 20:35:01.82336
2025-09-03 20:35:01.900432	135	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-04-21 20:35:01.900432
2025-09-03 20:35:01.980507	136	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-04-20 20:35:01.980507
2025-09-03 20:35:02.062764	137	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-04-19 20:35:02.062764
2025-09-03 20:35:02.140189	138	{"unit": "AH", "chargingAmpHrs": 0, "powerGeneration": 0, "maxChargingPower": 0, "powerConsumption": 0, "dischargingAmpHrs": 0, "maxBatteryVoltage": 0, "maxChargingCurrent": 0, "maxDischargingPower": 0, "maxDischargingCurrent": 0, "currentDayMinBatteryVoltage": 0}	2	2025-04-18 20:35:02.140189
\.


--
-- Data for Name: system_information; Type: TABLE DATA; Schema: device; Owner: postgres
--

COPY device.system_information (device_id, payload, created_at) FROM stdin;
\.


--
-- Data for Name: complex_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.complex_settings (id, param, value, created_at) FROM stdin;
\.


--
-- Name: command_history_id_seq; Type: SEQUENCE SET; Schema: device; Owner: postgres
--

SELECT pg_catalog.setval('device.command_history_id_seq', 191, true);


--
-- Name: complex_settings_id_seq; Type: SEQUENCE SET; Schema: device; Owner: postgres
--

SELECT pg_catalog.setval('device.complex_settings_id_seq', 12, true);


--
-- Name: dynamic_information_id_seq; Type: SEQUENCE SET; Schema: device; Owner: postgres
--

SELECT pg_catalog.setval('device.dynamic_information_id_seq', 476982, true);


--
-- Name: event_log_id_seq; Type: SEQUENCE SET; Schema: device; Owner: postgres
--

SELECT pg_catalog.setval('device.event_log_id_seq', 218, true);


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

