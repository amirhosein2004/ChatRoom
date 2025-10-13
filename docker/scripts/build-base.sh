#!/bin/bash

# Build script for ChatPage base Docker image
# This script builds the base image that other environments extend from

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="chatpage-base"
IMAGE_TAG="latest"
DOCKERFILE_PATH="docker/base/base.dockerfile"
BUILD_CONTEXT="."

echo -e "${BLUE}🐳 Building ChatPage Base Docker Image${NC}"
echo "=================================="

# Check if Dockerfile exists
if [ ! -f "$DOCKERFILE_PATH" ]; then
    echo -e "${RED}❌ Error: Dockerfile not found at $DOCKERFILE_PATH${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Build Configuration:${NC}"
echo "  Image Name: $IMAGE_NAME:$IMAGE_TAG"
echo "  Dockerfile: $DOCKERFILE_PATH"
echo "  Build Context: $BUILD_CONTEXT"
echo ""

# Remove existing image if it exists
echo -e "${YELLOW}🧹 Cleaning up existing image...${NC}"
if docker image inspect "$IMAGE_NAME:$IMAGE_TAG" >/dev/null 2>&1; then
    docker rmi "$IMAGE_NAME:$IMAGE_TAG" || true
    echo -e "${GREEN}✅ Removed existing image${NC}"
else
    echo -e "${BLUE}ℹ️  No existing image to remove${NC}"
fi

# Build the base image
echo -e "${YELLOW}🔨 Building base image...${NC}"
docker build \
    -f "$DOCKERFILE_PATH" \
    -t "$IMAGE_NAME:$IMAGE_TAG" \
    "$BUILD_CONTEXT"

# Verify the build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Base image built successfully!${NC}"
    echo -e "${BLUE}📊 Image Information:${NC}"
    docker images "$IMAGE_NAME:$IMAGE_TAG"
    
    # Show image size
    IMAGE_SIZE=$(docker images --format "table {{.Size}}" "$IMAGE_NAME:$IMAGE_TAG" | tail -n 1)
    echo -e "${BLUE}📦 Image Size: $IMAGE_SIZE${NC}"
    
    echo ""
    echo -e "${GREEN}🎉 ChatPage base image is ready for use!${NC}"
    echo -e "${BLUE}💡 You can now build environment-specific images that extend from this base.${NC}"
else
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi
