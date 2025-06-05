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
-- Name: command_history id; Type: DEFAULT; Schema: device; Owner: postgres
--

ALTER TABLE ONLY device.command_history ALTER COLUMN id SET DEFAULT nextval('device.command_history_id_seq'::regclass);


--
-- Name: dynamic_information id; Type: DEFAULT; Schema: device; Owner: postgres
--

ALTER TABLE ONLY device.dynamic_information ALTER COLUMN id SET DEFAULT nextval('device.dynamic_information_id_seq'::regclass);


--
-- Name: command_history command_history_pk; Type: CONSTRAINT; Schema: device; Owner: postgres
--

ALTER TABLE ONLY device.command_history
    ADD CONSTRAINT command_history_pk PRIMARY KEY (id);


--
-- Name: dynamic_information dynamic_information_pk; Type: CONSTRAINT; Schema: device; Owner: postgres
--

ALTER TABLE ONLY device.dynamic_information
    ADD CONSTRAINT dynamic_information_pk PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

