# LexAmoris
Lex amoris 

## Overview

LexAmoris (Nexus Martinique) is a transparent sovereignty platform that embodies the Law of Love concept. This static website showcases the vision of bio-distributed sovereign systems and sustainable living.

## Deployment

This project is configured for deployment on [Render.com](https://render.com) as a static site.

### Automatic Deployment

1. Connect your GitHub repository to Render
2. Render will automatically detect the `render.yaml` configuration
3. The site will be deployed with the following features:
   - Static file serving from the root directory
   - Security headers (X-Frame-Options, X-Content-Type-Options, X-XSS-Protection)
   - Caching configuration for optimal performance
   - Automatic HTTPS

### Manual Deployment

You can also deploy this as a simple static site on any web hosting platform:

1. Clone the repository
2. Upload all files to your web server
3. Ensure `index.html` is set as the default document
4. Configure HTTPS if your hosting supports it

### Local Development

To view the site locally:

1. Clone the repository: `git clone https://github.com/hannesmitterer/LexAmoris.git`
2. (Optional) Run the deployment validation script: `./deploy.sh`
3. Open `index.html` in your web browser
4. Alternatively, use a local web server:
   ```bash
   # Using Python 3
   python3 -m http.server 8000
   
   # Using Node.js (if you have npx)
   npx serve .
   ```
5. Access the site at `http://localhost:8000`

**Note**: The `deploy.sh` script is already executable. If you need to make it executable manually, run: `chmod +x deploy.sh`

## Project Structure

- `index.html` - Main website file
- `mission.md` - Project mission and vision statement
- `render.yaml` - Render.com deployment configuration
- `LICENSE` - Project license
- `README.md` - This file

## Features

- **Transparent Sovereignty**: Status dashboard showing sustainability metrics
- **S-ROI Index**: Transparency index visualization (0.5192)
- **Energy Status**: Renewable energy tracking
- **IPFS Integration**: Decentralized repository connection display
- **Responsive Design**: Mobile-friendly interface
- **Lex Amoris Signature**: Protection of the Law of Love active

## Technology Stack

- Pure HTML/CSS (no dependencies)
- Comfortaa font from Google Fonts
- Modern CSS with custom properties and animations
- Static hosting ready

## License

See [LICENSE](LICENSE) file for details.

## Author

Hannes Mitterer - *Sempre in Costante*
