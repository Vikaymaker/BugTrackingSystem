create database food_donation;
use food_donation;

-- Table for storing user information
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    informer_name VARCHAR(255) NOT NULL,
    informer_address VARCHAR(255) NOT NULL,
    informer_number VARCHAR(20) NOT NULL,
    needer_address VARCHAR(255) NOT NULL,
    landmark VARCHAR(255) NOT NULL,
    num_people INT NOT NULL
);



CREATE TABLE donations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization_name VARCHAR(255),
    food_type VARCHAR(255),
    quantity INT,
    donor_name VARCHAR(255),
    donor_address VARCHAR(255),
    donor_phone VARCHAR(20),
    donation_method VARCHAR(255),
    drop_off_location VARCHAR(255),
    received_from TEXT, -- Changed column name from "received" to "received_from"
    donated_for TEXT, -- Changed column name from "donated" to "donated_for"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);




CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    experience VARCHAR(50) NOT NULL,
    professionalism VARCHAR(50) NOT NULL,
    comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS volunteers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    location VARCHAR(255) NOT NULL
);

CREATE TABLE trust (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location TEXT NOT NULL,
    category TEXT NOT NULL,
    contact VARCHAR(20) NOT NULL
);

INSERT INTO trust (name, location, category, contact)
VALUES
('Anu Old Age Home', 'DRO Colony K Pudhur, Madurai', 'Institutions For Aged Charitable Old Age Homes', '09724318701'),
('Thaai Paravai Old Age Home', 'Vel Nagar Iyer Bungalow, Madurai', 'Institutions For Aged Charitable Old Age Homes', '08128852692'),
('Kirupa Old Age Home (Free Service)', 'Mangalakudi Village, Madurai', 'Institutions For Aged Charitable Old Age Homes', '08488925473'),
('Royal Vision', 'Perungudi Madurai City, Madurai', 'NGOS Charitable Trusts', '07942698483'),
('Anbu Suzh Ulagu Foundation', 'Madurai Road Tirumangalam, Madurai', 'Charitable Trusts', '07942698453'),
('Madurai Seed', 'Behind Gandhi Museum Karumbalai Gandhi Nagar, Madurai', 'Charitable Old Age Homes NGOS', '07942698542'),
('M S Perumal Social Trust Maravapatty', 'SREE BHARASAKTHI KALIYAMMAN KOVIL STREET Madurai, Madurai', 'Charitable Trusts Social Service Organisations', '07942698430'),
('Missionaries Of Charity Annai Teresa Illam', 'Opposite Fatima College Vilangudi, Madurai', 'NGOS Charitable Trusts', '07942698348'),
('Voluntary Association For People Service', 'Behind Ptr Mahal Chinna Chokkikulam, Madurai', 'NGOS Charitable Trusts', '07942698363'),
('Idhayam Charitable Trust', 'Ram Nagar, Madurai', 'Charitable Trusts', '07942698419'),
('Kaakum Karangal Charitable Trust', 'Thirunagar Police Station Opp St Thirunagar, Madurai', 'Charitable Trusts', '07942698212'),
('Mahasemam Trust', 'Melur, madurai', 'Charitable Trusts Health Care Centres', '07942698245'),
('M.D. CHARITABLE TRUST', 'NEAR SELVI HOMEOPATHY MEDICALS, madurai', 'NGOS Charitable Trusts', '07942698249'),
('Nikhil Foundation', 'Bharath Nagar Tiruppalai, Madurai', 'Charitable Old Age Homes NGOS', '07942698250'),
('Sri Rajarajeswari Amman Temple and Charitable Trust', 'Near Tvs Bus Stop Virattipathu, Madurai', 'Charitable Trusts', '07942698206'),
('She Welfare Trust', 'J P Kudil Usilampatti, Madurai', 'NGOS Charitable Trusts', '07942698083'),
('Akshaya''s Helping I H.E.L.P Trust', '1st Cross Street, Madurai', 'Orphanages Charitable Trusts', '07942698182'),
('Idhayam Trust', 'Opposite Ar Police Store Madurai Reserve Lines, Madurai', 'NGOS Charitable Trusts', '07942698112'),
('Joe Britto Educational And Social Trust', 'Kathakinaru, madurai', 'Charitable Trusts', '07942698174'),
('Madurai Charitable Trust', 'Near Keshavan Hospital, madurai', 'Charitable Trusts', '07942698111'),
('Sadhana Trust', 'Madurai Race Course, madurai', 'Charitable Old Age Homes NGOS', '07942697805'),
('Springs Of Life Charitable Trust', 'Pykara, Madurai', 'Charitable Trusts', '07942697961'),
('Masha Trust', 'rc church Anna Nagar Madurai, Madurai', 'Charitable Trusts Trustees', '07942697842'),
('LG Relax Home', 'Near By Golden Hospital Melamadai, madurai', 'Institutions For Aged Orphanages', '07942697799'),
('Elysium Foundation', 'Arignar Anna Nagar, Madurai', 'Charitable Trusts', '07942697764'),
('Bala Memorial Trust', 'Kurinji Nagar Near K B Yenthal Pillayar Kovil Andar Kottaram, Madurai', 'Charitable Trusts Welfare Organisations', '07942697732'),
('Thost Trust', 'Puthur Pudur Bazaar, Madurai', 'Charitable Trusts Research Centres', '07942697670');


CREATE TABLE contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELETE FROM donations WHERE id = 3;

select * from contacts;
select * from users;
select * from donations;
select * from requests;
select * from volunteers;
select * from feedback;
select * from trust;























CREATE TABLE donations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    organization VARCHAR(255) NOT NULL,
    specific_name VARCHAR(255) NOT NULL,
    food_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    quantity INT NOT NULL,
    donor_name VARCHAR(255) NOT NULL,
    donor_address TEXT NOT NULL,
    donor_phone VARCHAR(20) NOT NULL,
    donation_method VARCHAR(50) NOT NULL,
    location VARCHAR(255) NOT NULL,
    instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);