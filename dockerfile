# Use Nginx to serve static files
FROM nginx:alpine

# Copy all website files into Nginx folder
COPY ./ /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
