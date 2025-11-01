# QuizMe Buddy

This project helps you prepare for quizzes by generating questions from PDF documents and images.

## Prerequisites

### Option 1 : Run with Ollama Installed Locally 

1.  **Install Ollama:**
    *   Download and install Ollama from [https://ollama.ai/](https://ollama.ai/).
    *   Follow the installation instructions for your operating system.

2.  **Pull the Model:**
    *   This project uses the `qwen2.5vl:32b` model. or a smaller Visual Inference Model.
    *   Pull the model using the following command:
        ```bash
        ollama pull qwen2.5vl:32b
        ```
### Option 2 : Run with OpenAI or OpenAI compatible API (gemini)

refer `.env.example` on API Usage. Not Tested though.

### Python Environment with `uv`

This project uses `uv` for package management.

1.  **Install `uv`:**
    *   Follow the official installation instructions for `uv`: [https://github.com/astral-sh/uv#installation](https://github.com/astral-sh/uv#installation)

2.  **Create a Virtual Environment:**
    ```bash
    uv venv
    ```

3.  **Activate the Virtual Environment:**
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```

## Setup

1.  **Create a `.env` file:**
    *   Copy the `.env.example` file to a new file named `.env`:
        ```bash
        cp .env.example .env
        ```
    *   Update the `.env` file with your specific configurations.

2.  **Install Dependencies:**
    *   Use `uv sync` to install the dependencies listed in `pyproject.toml`:
        ```bash
        uv sync
        ```

## Usage

*   Run the main script to prepare the quiz:
    ```bash
    uv run python src/main-prepare-quiz.py
    ```

--- 


## Sample Output Analysing Pages on Acceleration from textBook
- Using Ollama:qwen2.5vl:32b running local.
- Study Material Physics-WEB_Sab7RrQ.pdf Pages 108, 109


---

### **Quiz on Acceleration: Key Concepts**


#### **Question 1: Understanding Acceleration and Velocity **

Which part of Figure 3.3 (a or b) is represented when the velocity vector is on the **positive side** of the scale and the acceleration vector is on the **negative side** of the scale? What does the car's motion look like for the given scenario?

1. **Part (a)**. The car is slowing down because the acceleration and the velocity vectors are acting in the **opposite direction**.
2. **Part (a)**. The car is speeding up because the acceleration and the velocity vectors are acting in the **same direction**.
3. **Part (b)**. The car is slowing down because the acceleration and the velocity vectors are acting in the **same direction**.
4. **Part (b)**. The car is speeding up because the acceleration and the velocity vectors are acting in the **opposite direction**.

**Answer: A**

---

#### **Explanation:**
- In Figure 3.3, **part (a)** shows the car speeding up (positive acceleration and positive velocity), while **part (b)** shows the car slowing down (negative acceleration and positive velocity).
- If the velocity vector is positive and the acceleration vector is negative, it indicates that the car is slowing down (negative acceleration opposes the direction of velocity). This corresponds to **part (b)**.

---

#### **Question 2: Identifying Acceleration Types**

Which type of acceleration is being measured when we calculate the average acceleration over a period of time?

1. **Instantaneous acceleration** because it occurs at a specific instant in time.
2. **Negative acceleration** because it always opposes the direction of velocity.
3. **Average acceleration** because it is the change in velocity divided by the total time interval.
4. **Positive acceleration** because it always indicates speeding up.

**Answer: C**

---

#### **Explanation:**
- The text in the image defines **average acceleration** as the change in velocity divided by the total time interval. This is calculated using the formula:
  \[
  \bar{a} = \frac{\Delta v}{\Delta t} = \frac{v_f - v_i