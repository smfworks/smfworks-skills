#!/bin/bash
#
# SMF Works Skills - Installation Script
# One-liner: curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash
#

set -e

SMF_DIR="$HOME/.smf"
BIN_DIR="$HOME/.local/bin"
REPO_URL="https://github.com/smfworks/smfworks-skills.git"

# Detect if we're being called as 'smfw' or 'smf'
SCRIPT_NAME="$(basename "$0")"

# Check for ClawHub conflict
CLAWHUB_SMF="$(which smf 2>/dev/null || echo "")"
if [ -n "$CLAWHUB_SMF" ] && [[ "$CLAWHUB_SMF" == *"clawhub"* ]]; then
    echo "⚠️  Detected ClawHub CLI also provides 'smf' command."
    echo "   Installing as 'smfw' to avoid conflicts."
    echo ""
    INSTALL_AS="smfw"
else
    # Install both for backward compatibility
    INSTALL_AS="both"
fi

echo "🔧 Installing SMF Works Skills CLI..."

# Create directories
mkdir -p "$SMF_DIR/skills"
mkdir -p "$BIN_DIR"

# Check if smf CLI already exists
if [ -f "$BIN_DIR/smf" ] || [ -f "$BIN_DIR/smfw" ]; then
    echo "⚠️  SMF CLI already installed. Updating..."
fi

# Download smf CLI
echo "📥 Downloading SMF CLI..."
curl -fsSL "https://raw.githubusercontent.com/smfworks/smfworks-skills/main/cli/smf" -o "$BIN_DIR/smf"
chmod +x "$BIN_DIR/smf"

# Also install as 'smfw' (preferred name to avoid conflicts)
cp "$BIN_DIR/smf" "$BIN_DIR/smfw"
chmod +x "$BIN_DIR/smfw"

echo "✅ Installed: smf (legacy), smfw (preferred)"

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
    
    # Check if already in shell rc
    if ! grep -q "$BIN_DIR" "$SHELL_RC" 2>/dev/null; then
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"
        echo "✅ Added to PATH in $SHELL_RC"
        echo "   Run: source $SHELL_RC"
    fi
fi

echo ""
echo "✅ SMF CLI installed successfully!"
echo ""
echo "⚠️  IMPORTANT: Use 'smfw' instead of 'smf' to avoid conflicts with ClawHub CLI."
echo ""
echo "Next steps:"
echo "  1. Install a skill:   smfw install file-organizer"
echo "  2. Run the skill:     smfw run file-organizer --help"
echo "  3. List all skills:   smfw list"
echo ""
echo "For Pro skills, login first:"
echo "  smfw login"
echo ""
echo "Documentation: https://github.com/smfworks/smfworks-skills"
echo ""
echo "Note: 'smf' command still works but may conflict with ClawHub."
echo "      Prefer 'smfw' for reliable operation."
