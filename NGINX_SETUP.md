## Nginx and SSL Setup

### Nginx Setup
To setup Nginx as a reverse proxy for the bot:

1. Install Nginx:
```bash
sudo apt update
sudo apt install nginx
```

2. Copy the provided nginx.conf to Nginx sites:
```bash
sudo cp nginx.conf /etc/nginx/sites-available/tg-file2link
sudo ln -s /etc/nginx/sites-available/tg-file2link /etc/nginx/sites-enabled/
```

3. Set your domain name (replace example.com with your domain):
```bash
sudo sed -i 's/server_name example.com/server_name yourdomain.com/g' /etc/nginx/sites-available/tg-file2link
```

4. Configure download speed limit (default is 1MB/s, change to your desired speed):
```bash
# For example, to set 2MB/s limit:
sudo sed -i 's/limit_rate 1m/limit_rate 2m/g' /etc/nginx/sites-available/tg-file2link

# Or to set 500KB/s limit:
sudo sed -i 's/limit_rate 1m/limit_rate 500k/g' /etc/nginx/sites-available/tg-file2link
```

5. Test and restart Nginx:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

Note: The rate limiting configuration includes:
- Request rate: 10 requests per second with burst of 20
- Connection limit: 10 concurrent connections per IP
- Download speed: Configurable per connection (default 1MB/s)

### SSL Setup with Certbot

To secure your site with HTTPS:

1. Install Certbot:
```bash
sudo apt install certbot python3-certbot-nginx
```

2. Get SSL certificate (replace example.com with your domain):
```bash
sudo certbot --nginx -d example.com
```

3. Auto-renewal (Certbot creates this automatically):
```bash
sudo certbot renew --dry-run
```

The certificates will auto-renew every 60 days. You can force renewal with:
```bash
sudo certbot renew
```

Note: Make sure your domain's DNS is properly configured and pointing to your server before running Certbot.
