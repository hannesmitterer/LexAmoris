# LexAmoris Dockerfile - Bio-Distributed Sovereign Stack
# This container serves the Lex Amoris documentation and web interface
# with provisions for future IPFS and Mycelium bio-synthetic integration

FROM nginx:alpine

# Metadata
LABEL maintainer="Lex Amoris Project"
LABEL description="Transparent Sovereignty - Bio-Distributed System"
LABEL version="1.0"

# Copy web files to nginx
COPY index.html /usr/share/nginx/html/
COPY mission.md /usr/share/nginx/html/
COPY README.md /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
