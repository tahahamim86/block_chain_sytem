# 🩺 Blockchain-Based Medical Diagnosis API

This Django REST API project provides a secure, token-based way for external app users to access their medical diagnosis documents. It ensures data integrity by maintaining a blockchain-like structure for each diagnosis using hashed blocks.

---

## 🚀Features

- 🔐 **Token-Based Authentication**: External users can set and validate access tokens.
- 📄 **Medical Records Access**: Users can retrieve their diagnosis documents using a valid token.
- 🔗 **Blockchain Verification**: Each diagnosis is associated with a block that stores a cryptographic hash to ensure data has not been tampered with.
- 🛠 **Automatic Blockchain Rebuild**: The blockchain is re-verified every time records are accessed.

---

## 🧠 How It Works

### 1. **ExternalAppUser**
Represents a user from an external system with standard attributes like name, email, and password.

### 2. **AccessToken**
Links an `ExternalAppUser` to a token used for authentication.

### 3. **MedicalRecord**
A one-to-one link between a user and their overall medical history.

### 4. **DiseaseDiagnosis**
Each diagnosis entry contains details like disease name, date, and optional images.

### 5. **DiagnosisBlock**
Each diagnosis is wrapped in a block that contains a hash and a reference to the previous hash — forming a basic blockchain.

---

##  API Endpoints

### `GET /check_user_token/<app_user_id>/`
Check whether a token exists for a given user.

### `POST /set_user_token/`
Set or update a token for a user.

**Request Body:**
```json
{
  "app_user_id": 1,
  "token": "secure_token_123"
}
