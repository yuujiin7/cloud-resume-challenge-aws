# Use an official Nginx base image
FROM nginx:alpine

# Set the working directory to the web server root
WORKDIR /usr/share/nginx/html

# Copy the contents of your static website to the image
COPY ./resume-site/ .

# (Other optional configurations if needed)

# The CMD instruction sets the command to be executed when the container starts
CMD ["nginx", "-g", "daemon off;"]
