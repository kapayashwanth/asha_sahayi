-- db.sql
-- ASHA Sahayi Database Schema (MySQL)

-- Create database
CREATE DATABASE IF NOT EXISTS asha_sahayi;
USE asha_sahayi;

-- =========================
-- ASHA WORKERS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS asha_workers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    asha_id VARCHAR(20),
    phone VARCHAR(15),
    preferred_language VARCHAR(10) DEFAULT 'en',
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- PATIENT VISITS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS patient_visits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asha_id INT NOT NULL,
    patient_age INT,
    category ENUM('Pregnancy', 'Child Health', 'Nutrition', 'General') DEFAULT 'General',
    symptoms TEXT,
    action_taken VARCHAR(255),
    referral_required BOOLEAN DEFAULT FALSE,
    visit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asha_id)
        REFERENCES asha_workers(id)
        ON DELETE CASCADE
);

-- =========================
-- AI QUERIES TABLE
-- =========================
CREATE TABLE IF NOT EXISTS ai_queries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asha_id INT,
    query_text TEXT,
    response_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asha_id)
        REFERENCES asha_workers(id)
        ON DELETE SET NULL
);

-- =========================
-- INDEXES (OPTIONAL)
-- =========================
CREATE INDEX idx_asha_telegram ON asha_workers(telegram_id);
CREATE INDEX idx_visit_date ON patient_visits(visit_date);
CREATE INDEX idx_ai_date ON ai_queries(created_at);
