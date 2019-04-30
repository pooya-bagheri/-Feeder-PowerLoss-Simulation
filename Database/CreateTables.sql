-- Following SQL scripts will create blank tables for the DB recording simulation results
CREATE TABLE Instants (
    InstantID int NOT NULL,
    Day int NOT NULL,
    Hour int NOT NULL,
    Minute int NOT NULL,
    Second int NOT NULL,
    PRIMARY KEY (InstantID)
);
CREATE TABLE Nodes (
    NodeID int NOT NULL,
    Bus Text NOT NULL,
    Phase int NOT NULL,
    PRIMARY KEY (NodeID)
);
CREATE TABLE Losses (
    InstantID int NOT NULL,
    Ploss real NOT NULL,
    FOREIGN KEY (InstantID) REFERENCES Instants(InstantID)
    PRIMARY KEY (InstantID)
);
CREATE TABLE Voltages (
    InstantID int NOT NULL,
    NodeID int NOT NULL,
    Vmag real NOT NULL,
    Vang real NOT NULL,
    FOREIGN KEY (InstantID) REFERENCES Instants(InstantID)
    FOREIGN KEY (NodeID) REFERENCES Nodes(NodeID)
    PRIMARY KEY (InstantID,NodeID)
);
CREATE TABLE LoadProfiles (
    InstantID int NOT NULL,
    LoadID int NOT NULL,
    Scale real NOT NULL,
    FOREIGN KEY (InstantID) REFERENCES Instants(InstantID)
    FOREIGN KEY (LoadID) REFERENCES Loads(LoadID)
    PRIMARY KEY (InstantID,LoadID)
);