-- 1. 사용자 테이블
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255),
    name VARCHAR(100),
    birth DATE,
    role ENUM('consumer', 'supplier', 'admin'),
    supplier_id INT,
    is_verified BOOLEAN DEFAULT FALSE,
    email_verification_token VARCHAR(255),
    social_provider VARCHAR(50),
    social_id VARCHAR(255),
    terms_version_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reset_password_token VARCHAR(255),
    reset_password_expires_at DATETIME
);

-- 2. 공급자
CREATE TABLE suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    address VARCHAR(255),
    business_license_number VARCHAR(100),
    is_verified BOOLEAN DEFAULT FALSE,
    image_url VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. 알러지
CREATE TABLE allergens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- 4. 음식
CREATE TABLE foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ingredient TEXT,
    image_url VARCHAR(255),
    source_type ENUM('user', 'ocr', 'crowl') NOT NULL,
    supplier_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

-- 5. 바코드
CREATE TABLE barcodes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(255) NOT NULL,
    food_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES foods(id)
);

-- 6. 번들
CREATE TABLE food_bundles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image_url VARCHAR(255),
    supplier_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

-- 7. food_bundle_items
CREATE TABLE food_bundle_items (
    bundle_id INT NOT NULL,
    food_id INT NOT NULL,
    PRIMARY KEY (bundle_id, food_id),
    FOREIGN KEY (bundle_id) REFERENCES food_bundles(id),
    FOREIGN KEY (food_id) REFERENCES foods(id)
);

-- 8. QR 링크
CREATE TABLE qr_links (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(255) NOT NULL,
    type ENUM('food', 'bundle', 'supplier'),
    food_id INT NOT NULL,
    bundle_id INT NOT NULL,
    supplier_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES foods(id),
    FOREIGN KEY (bundle_id) REFERENCES food_bundles(id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

-- 9. 즐겨찾기
CREATE TABLE favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    food_id INT,
    bundle_id INT,
    supplier_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    FOREIGN KEY (bundle_id) REFERENCES food_bundles(id) ON DELETE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE CASCADE
);

-- 10. 조회 로그
CREATE TABLE view_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type ENUM('food', 'bundle', 'supplier'),
    food_id INT,
    bundle_id INT,
    supplier_id INT,
    viewed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    FOREIGN KEY (bundle_id) REFERENCES food_bundles(id) ON DELETE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE CASCADE
);

-- 11. food_allergens (N:N)
CREATE TABLE food_allergens (
    food_id INT NOT NULL,
    allergen_id INT NOT NULL,
    PRIMARY KEY (food_id, allergen_id),
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    FOREIGN KEY (allergen_id) REFERENCES allergens(id) ON DELETE CASCADE
);

-- 12. user_allergens (N:N)
CREATE TABLE user_allergens (
    user_id INT NOT NULL,
    allergen_id INT NOT NULL,
    PRIMARY KEY (user_id, allergen_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (allergen_id) REFERENCES allergens(id) ON DELETE CASCADE
);

ALTER TABLE foods
ADD COLUMN registered_by_user_id INT NOT NULL,
ADD CONSTRAINT fk_foods_users FOREIGN KEY (registered_by_user_id) REFERENCES users(id);

-- supplier id = 1은 consumer 등록이라는 의미임임
INSERT INTO suppliers (id, name, created_at)
VALUES (1, 'default supplier', NOW());