# Production Dockerfile for ChatPage
# Optimized for production deployment with security and performance

FROM chatpage-base:latest

# Switch to root to copy entrypoint script
USER root

# Install production dependencies
RUN pip install --no-cache-dir -r requirements/production.txt

# Make entrypoint script executable
RUN chmod +x /app/docker/scripts/entrypoint.sh

# Set ownership
RUN chown appuser:appuser /app/docker/scripts/entrypoint.sh

# Switch back to app user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run entrypoint script
ENTRYPOINT ["/app/docker/scripts/entrypoint.sh"]
