-- 공급자 테이블
CREATE TABLE suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    business_license_number VARCHAR(100),       -- 사업자 번호 (선택)
    is_verified BOOLEAN DEFAULT FALSE,           -- 인증 여부
    image_url VARCHAR(255),                -- 공급자 이미지 URL (선택)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 사용자 테이블
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    name VARCHAR(100),
    birth DATE NOT NULL, -- 생년월일 입력 형식을 'xxxx-xx-xx'로 하거나 STR_TO_DATE('20010402', '%Y%m%d')로 하거나 선택.
    role ENUM('consumer', 'supplier', 'admin') NOT NULL,
    supplier_id INT DEFAULT NULL,                -- 공급자 ID (소비자일 경우 NULL)
    is_verified BOOLEAN DEFAULT FALSE,           -- 이메일 인증 여부
    email_verification_token VARCHAR(255),       -- 이메일 인증용 토큰 (선택)
    social_provider VARCHAR(50),                 -- 예: 'google'
    social_id VARCHAR(255),                      -- 소셜 로그인용 ID
    terms_version_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL,
    FOREIGN KEY (terms_version_id) REFERENCES terms_versions(id) ON DELETE SET NULL
);

-- 알러지 항목 테이블
CREATE TABLE allergens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- 사용자-알러지 매핑 테이블
CREATE TABLE user_allergens (
    user_id INT,
    allergen_id INT,
    PRIMARY KEY (user_id, allergen_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (allergen_id) REFERENCES allergens(id) ON DELETE CASCADE
);

-- 식품 테이블 -> 식품에서 바코를 따로 빼서 API에 맞게 따로 테이블
CREATE TABLE foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image_url VARCHAR(255), -- 이미지 URL (선택)
    supplier_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE CASCADE
);

-- 성분 테이블
CREATE TABLE ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- 식품-성분 매핑 테이블
CREATE TABLE food_ingredients (
    food_id INT,
    ingredient_id INT,
    PRIMARY KEY (food_id, ingredient_id),
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE
);

-- 성분-알러지 매핑 테이블
CREATE TABLE ingredient_allergens (
    ingredient_id INT,
    allergen_id INT,
    PRIMARY KEY (ingredient_id, allergen_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE,
    FOREIGN KEY (allergen_id) REFERENCES allergens(id) ON DELETE CASCADE
);

-- 묶음 상품 테이블
CREATE TABLE food_bundles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image_url VARCHAR(255), -- 이미지 URL (선택)
    supplier_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE CASCADE
);

-- 묶음 구성 테이블
CREATE TABLE food_bundle_items (
    bundle_id INT,
    food_id INT,
    PRIMARY KEY (bundle_id, food_id),
    FOREIGN KEY (bundle_id) REFERENCES food_bundles(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE
);

-- QR 코드 링크 테이블
CREATE TABLE qr_links (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(255) UNIQUE NOT NULL,
    type ENUM('food', 'bundle', 'supplier') NOT NULL,
    food_id INT,
    bundle_id INT,
    supplier_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_food FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    CONSTRAINT fk_bundle FOREIGN KEY (bundle_id) REFERENCES food_bundles(id) ON DELETE CASCADE,
    CONSTRAINT fk_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE CASCADE,
);

-- 식품 바코드 테이블
CREATE TABLE barcodes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(64) UNIQUE NOT NULL,
    food_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE
);

-- 섭취 기록 테이블
CREATE TABLE intake_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    food_id INT,
    intake_time DATETIME,
    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack'),
    reaction_score INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE SET NULL
);

-- 증상 기록 테이블
CREATE TABLE symptoms_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    log_time DATETIME,
    symptoms TEXT,
    severity INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 즐겨찾기 테이블
CREATE TABLE favorites (
    user_id INT,
    food_id INT,
    PRIMARY KEY (user_id, food_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE
);

-- OCR 결과 저장 테이블
CREATE TABLE ocr_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    input_food_name VARCHAR(255),,
    suggested_food_name VARCHAR(255),
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 식품 조회 이력 테이블
CREATE TABLE view_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    food_id INT,
    viewed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE
);

-- 동의 약관 테이블(new)
CREATE TABLE terms_versions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    version VARCHAR(20) NOT NULL, -- 예: '1.0', '1.1'
    content TEXT NOT NULL, -- 약관 원문 (필요 시 Markdown/HTML)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE -- 현재 유효한 버전 표시
);