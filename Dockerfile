FROM python:3.11-bullseye

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies (creates .venv)
RUN uv sync --frozen

# Ensure venv binaries are used
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code

COPY . .

#Expose the port for streamlit users
EXPOSE 8501


# Run streamlit app
CMD ["streamlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8501"]