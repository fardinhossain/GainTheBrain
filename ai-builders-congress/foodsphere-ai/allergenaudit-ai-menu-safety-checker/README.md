# 🛡️ AllergenAudit AI: Automated Menu-to-Ingredient Safety Cross-Checker

## Category / Domain
FoodSphere AI (Food Safety / Restaurant Tech)

## Date
2026-09-19

## Short Description
AllergenAudit AI is an intelligent compliance platform that automatically synchronizes restaurant menus with raw ingredient invoices to ensure allergen disclosures are 100% accurate and up-to-date.

## Problem Statement
Food allergies are a major public health concern, yet restaurant allergen charts are often static, paper-based, and rarely updated when a chef changes a brand of sauce or a supplier substitutes an ingredient. This "documentation lag" leads to life-threatening risks for customers and massive legal liabilities for food service businesses. Manually auditing every ingredient in every dish against a menu is labor-intensive and prone to human error.

## Proposed Solution
The platform uses OCR (Optical Character Recognition) to scan supplier invoices and delivery notes, extracting specific ingredient lists and sub-components. An AI engine then cross-references these ingredients against the restaurant's digital menu items. If a new allergen is detected (e.g., a new brand of mayo contains mustard or soy not previously listed), the system flags the dish and automatically suggests an update to the digital menu and kitchen staff alerts.

## Target Users
- **Restaurant Managers:** To ensure legal compliance and customer safety.
- **Executive Chefs:** To track ingredient changes across multiple locations.
- **Food Safety Auditors:** To perform rapid, data-driven inspections.
- **Hospitality Groups:** To maintain standardized safety protocols across chains.

## Core Features
- **Invoice OCR Pipeline:** Upload PDFs or photos of supplier invoices to extract product names and ingredient lists.
- **Menu Mapping Engine:** Link specific raw ingredients to final menu items (e.g., "Brioche Buns" linked to "Classic Burger").
- **Allergen Detection:** Automatic identification of the "Big 9" allergens (Milk, Eggs, Fish, Crustacean shellfish, Tree nuts, Peanuts, Wheat, Soybeans, and Sesame).
- **Discrepancy Alerts:** Real-time notifications when a change in supplier data contradicts the current menu's allergen labels.
- **Compliance Dashboard:** A bird's-eye view of all menu items and their current safety status.

## Advanced Features
- **Supplier Recall Integration:** Automatically flag menu items if a specific ingredient batch is listed in a national FDA/USDA recall database.
- **Dynamic QR Menus:** Generate customer-facing digital menus that update in real-time based on the current validated ingredient list.
- **Substitution Recommender:** Suggest alternative ingredients from a pre-approved list that maintain the dish's allergen-free profile.
- **Multi-Location Sync:** Push ingredient changes across a franchise network instantly.

## AI/ML Integration
- **NLP Entity Extraction:** Using LLMs (e.g., GPT-4o or Claude 3.5) to parse complex, semi-structured ingredient labels and identify hidden allergens (e.g., recognizing that "Casein" implies "Milk").
- **OCR Refinement:** Fine-tuning vision models to handle low-quality photos of thermal-printed kitchen receipts and invoices.
- **Categorization Logic:** Probabilistic matching between vague invoice descriptions (e.g., "Chef's Choice Oil") and their likely allergen components based on historical data.

## Suggested Tech Stack
- **Frontend:** React.js or Next.js with Tailwind CSS for a responsive dashboard.
- **Backend:** Python (FastAPI) for high-performance AI processing.
- **OCR Service:** AWS Textract or Google Document AI for robust invoice parsing.
- **AI Model:** OpenAI API (GPT-4o-mini) for ingredient analysis and allergen mapping.
- **Database:** PostgreSQL for structured menu and ingredient relations.
- **Cache:** Redis for managing real-time alert queues.

## Database Design
- **Restaurants:** `id, name, location, api_key`
- **Menu_Items:** `id, restaurant_id, name, description, current_allergen_flags`
- **Ingredients:** `id, name, raw_text_label, detected_allergens, supplier_id`
- **Recipe_Links:** `menu_item_id, ingredient_id` (Many-to-Many)
- **Audit_Logs:** `id, timestamp, menu_item_id, change_detected, resolved_status`

## API Route Ideas
- `POST /api/v1/invoices/upload`: Processes a file and extracts ingredient data.
- `GET /api/v1/menu/audit`: Returns a list of menu items with allergen discrepancies.
- `PATCH /api/v1/menu/{id}/update-allergens`: Manually or automatically resolves a flag.
- `GET /api/v1/public/menu/{slug}`: Fetches the real-time validated menu for customers.

## UI Pages
- **Overview Dashboard:** Stats on recent deliveries, pending flags, and safety health score.
- **Digital Recipe Book:** Interface to link ingredients to dishes.
- **Invoice History:** A searchable archive of processed supplier documents.
- **Customer Menu View:** A clean, accessible page for diners to filter by their specific allergies.

## MVP Plan
1. Build the OCR pipeline to extract text from a single supplier's invoice format.
2. Implement the LLM logic to identify the Big 9 allergens from raw text strings.
3. Create a simple CRUD for a menu and a linking system to ingredients.
4. Develop the "Discrepancy Engine" that triggers an alert when a link is broken.
5. Launch a basic dashboard to view alerts.

## Future Scope
- **Nutritional Tracking:** Expand from allergens to full macro/micro-nutrient tracking for health-conscious restaurants.
- **Inventory Integration:** Sync with POS systems (Toast, Square) to track ingredient depletion and shelf-life.
- **Voice-Activated Kitchen Assistant:** Allow chefs to ask "Is the current batch of mayo soy-free?" via smart speakers.

## Difficulty Level
Intermediate (Requires solid knowledge of OCR, LLM prompt engineering, and relational database management).

## Portfolio Value
- Demonstrates high-impact use of AI for public safety.
- Showcases ability to handle unstructured data (invoices) and transform it into structured business logic.
- Highly relevant to the massive Food-Tech and SaaS industries.

## Possible Monetization
- **SaaS Subscription:** Monthly fee per restaurant location.
- **Enterprise Tier:** For large catering companies or hospital cafeterias.
- **API Licensing:** For POS providers who want to integrate allergen auditing into their ecosystem.

## Learning Outcomes
- Mastering document processing and OCR workflows.
- Learning to use LLMs for high-precision classification tasks.
- Designing complex many-to-many relationships in a relational database.
- Understanding the regulatory landscape of food safety (HACCP, FDA guidelines).
