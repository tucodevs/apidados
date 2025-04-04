CREATE TABLE tipos_eventos (
    EventTypeId BIGINT PRIMARY KEY,
    EventType VARCHAR(100),
    Description TEXT,
    DisplayUnits VARCHAR(50),
    FormatType VARCHAR(50),
    ValueName VARCHAR(100)
);

CREATE TABLE tr_excesso_velocidade_55km_2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    AssetId BIGINT,
    DriverId BIGINT,
    EventId BIGINT,
    EventTypeId BIGINT,
    EventCategory VARCHAR(100),
    StartDateTime DATETIME,
    StartLatitude DECIMAL(10,8),
    StartLongitude DECIMAL(11,8),
    StartSpeedKph DECIMAL(6,2),
    StartOdometer DECIMAL(10,2),
    EndDateTime DATETIME,
    EndLatitude DECIMAL(10,8),
    EndLongitude DECIMAL(11,8),
    EndSpeedKph DECIMAL(6,2),
    EndOdometer DECIMAL(10,2),
    Value DECIMAL(10,6),
    FuelUsedLitres DECIMAL(10,6),
    ValueType VARCHAR(100),
    ValueUnits VARCHAR(100),
    TotalTimeSeconds INT,
    TotalOccurances INT,
    SpeedLimit INT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (EventTypeId) REFERENCES tipos_eventos(EventTypeId)
);

CREATE TABLE tr_fora_faixa_verde LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_excesso_velocidade_30km LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_batendo_transmissao LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_excesso_velocidade_40km_2 LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_embreagem_acionada_indevida LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_freada_brusca_grave LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_aceleracao_brusca LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_marcha_lenta_5min LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_excesso_velocidade_20km LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_freada_brusca LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_excesso_velocidade_60km LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_excesso_rpm_parado LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_marcha_lenta LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_curva_brusca LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_excesso_velocidade_50km LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_inercia_aproveitada LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_excesso_velocidade_40km_1 LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_excesso_velocidade_55km_1 LIKE tr_excesso_velocidade_55km_2;
CREATE TABLE tr_excesso_rotacao LIKE tr_excesso_velocidade_55km_2;
