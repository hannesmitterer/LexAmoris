# LexAmoris Deployment Guide

## Quick Start

LexAmoris is a static website that can be deployed to any static hosting platform. This guide covers the recommended deployment method using Render.com, as well as alternative options.

## Prerequisites

- A GitHub account with access to the LexAmoris repository
- (Optional) A Render.com account for automated deployments

## Deployment Options

### Option 1: Render.com (Recommended)

Render.com provides free static site hosting with automatic deployments from GitHub.

#### Setup Steps:

1. **Connect to Render**
   - Go to [render.com](https://render.com) and sign up/login
   - Click "New +" and select "Static Site"
   - Connect your GitHub account and select the LexAmoris repository

2. **Configure Deployment**
   - Render will automatically detect the `render.yaml` configuration
   - Name: `lexamoris` (or your preferred name)
   - Branch: `main` (or your preferred branch)
   - Build Command: (leave empty - no build needed)
   - Publish Directory: `.` (current directory)

3. **Deploy**
   - Click "Create Static Site"
   - Render will automatically deploy your site
   - You'll receive a URL like `https://lexamoris.onrender.com`

4. **Custom Domain (Optional)**
   - Go to your site settings in Render
   - Add your custom domain under "Custom Domains"
   - Configure your DNS as instructed by Render

#### Automatic Updates

Once configured, Render will automatically redeploy your site whenever you push changes to your connected branch.

### Option 2: Netlify

1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect to GitHub and select the LexAmoris repository
4. Settings:
   - Build command: (leave empty)
   - Publish directory: `.`
5. Click "Deploy site"

### Option 3: GitHub Pages

1. Go to your repository settings on GitHub
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select your branch (e.g., `main`)
4. Select `/` (root) as the folder
5. Click "Save"
6. Your site will be available at `https://[username].github.io/LexAmoris`

### Option 4: Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - Framework Preset: Other
   - Build Command: (leave empty)
   - Output Directory: `.`
5. Click "Deploy"

### Option 5: Traditional Web Hosting

For traditional web hosts (shared hosting, VPS, etc.):

1. Clone or download the repository
2. Upload all files to your web server's public directory (e.g., `public_html`, `www`)
3. Ensure `index.html` is in the root of your web directory
4. Configure HTTPS through your hosting provider's control panel

## Configuration Files

### render.yaml

The `render.yaml` file contains the deployment configuration for Render.com:

- **Type**: Static web service
- **Build Command**: None (pure HTML/CSS)
- **Publish Path**: Root directory
- **Security Headers**: Configured for security best practices
- **Caching**: 1 hour cache for static assets

### deploy.sh

An initialization script that:
- Validates the project structure
- Checks for required files
- Verifies HTML and YAML syntax
- Provides deployment information

To run the script:

```bash
./deploy.sh
```

## Environment Variables

This project does not require any environment variables as it's a static site. The `render.yaml` includes a `NODE_VERSION` variable for compatibility, but it's not actively used.

## Security Features

The deployment configuration includes security headers:

- `X-Frame-Options`: SAMEORIGIN (prevents clickjacking)
- `X-Content-Type-Options`: nosniff (prevents MIME-type sniffing)
- Automatic HTTPS on supported platforms

## Performance Optimization

- **Caching**: Static assets are cached for 1 hour
- **CDN**: Platforms like Render, Netlify, and Vercel provide global CDN
- **Compression**: Automatic gzip/brotli compression on most platforms
- **HTTPS**: Automatic SSL certificates

## Monitoring and Maintenance

### Render.com
- View deployment logs in the Render dashboard
- Monitor uptime and performance metrics
- Set up notifications for deployment failures

### General
- Monitor site availability using tools like UptimeRobot or Pingdom
- Check browser console for JavaScript errors (though this site has none)
- Validate HTML periodically using W3C Validator

## Troubleshooting

### Site not loading
- Check that `index.html` is in the correct directory
- Verify deployment logs for errors
- Ensure DNS settings are correct (for custom domains)

### Styling issues
- Verify the Google Fonts link is working
- Check browser console for CSS errors
- Clear browser cache

### Deployment fails
- Run `./deploy.sh` locally to validate files
- Check `render.yaml` syntax
- Review deployment logs for specific errors

## Local Testing

Before deploying, test locally:

```bash
# Using Python 3
python3 -m http.server 8000

# Using Node.js
npx serve .

# Using PHP
php -S localhost:8000
```

Then open `http://localhost:8000` in your browser.

## Rollback

If a deployment introduces issues:

### Render.com
1. Go to your site dashboard
2. Click "Deploys" in the left sidebar
3. Find the last working deployment
4. Click "..." → "Redeploy"

### Git-based Rollback
```bash
git revert HEAD
git push
```

## Continuous Integration (CI)

For automated testing before deployment, you can add a GitHub Actions workflow:

1. Create `.github/workflows/test.yml`
2. Add HTML validation steps
3. Run on pull requests and pushes

Example workflow (optional):

```yaml
name: Validate HTML
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install HTML validator
        run: npm install -g html-validator-cli
      - name: Validate HTML
        run: html-validator --file=index.html --verbose
```

## Support

For issues related to:
- **Deployment**: Check platform-specific documentation
- **Project**: Open an issue on GitHub
- **Content**: Contact the project maintainer

## Additional Resources

- [Render.com Documentation](https://render.com/docs/static-sites)
- [Netlify Documentation](https://docs.netlify.com/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Vercel Documentation](https://vercel.com/docs)

---

*Lex Amoris Signature: Protection of the Law of Love active.*  
*Sempre in Costante | Hannes Mitterer*
