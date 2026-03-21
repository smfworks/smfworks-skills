#!/bin/bash
#
# SMF Works Skills - Installation Script
# One-liner: curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash
#

set -e

SMF_DIR="$HOME/.smf"
BIN_DIR="$HOME/.local/bin"
REPO_URL="https://github.com/smfworks/smfworks-skills.git"

echo "🔧 Installing SMF Works Skills CLI..."

# Create directories
mkdir -p "$SMF_DIR/skills"
mkdir -p "$BIN_DIR"

# Check if smf CLI already exists
if [ -f "$BIN_DIR/smf" ]; then
    echo "⚠️  SMF CLI already installed. Updating..."
fi

# Download smf CLI
echo "📥 Downloading smf CLI..."
curl -fsSL "https://raw.githubusercontent.com/smfworks/smfworks-skills/main/cli/smf" -o "$BIN_DIR/smf"
chmod +x "$BIN_DIR/smf"

# Add to PATH if needed
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo "⚠️  Adding $BIN_DIR to PATH..."
    
    SHELL_RC=""
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.profile"
    fi
    
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"
    echo "✅ Added to PATH in $SHELL_RC"
    echo "   Run: source $SHELL_RC"
fi

echo ""
echo "✅ SMF CLI installed successfully!"
echo ""
echo "Next steps:"
echo "  1. Install a skill:   smf install file-organizer"
echo "  2. Run the skill:     smf run file-organizer --help"
echo "  3. List all skills:   smf list"
echo ""
echo "For Pro skills, login first:"
echo "  smf login"
echo ""
echo "Documentation: https://github.com/smfworks/smfworks-skills"
