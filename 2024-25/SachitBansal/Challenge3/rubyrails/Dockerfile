# Use a specific Ruby version (ensure it's compatible with Rails 5.1.4)
FROM ruby:2.4

# Install dependencies
RUN apt-get update -qq && apt-get install -y \
    nodejs \
    sqlite3 \
    libsqlite3-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    build-essential

# Set up working directory
WORKDIR /app

# Install bundler (specific version to match your Gemfile.lock)
RUN gem install bundler -v '1.17.3'

# Copy Gemfile and Gemfile.lock
COPY Gemfile /app/Gemfile
COPY Gemfile.lock /app/Gemfile.lock

# Install the gems
RUN bundle install

# Copy the rest of the application code
COPY . /app
# Precompile assets
RUN RAILS_ENV=production bundle exec rake assets:precompile
# Expose the default Rails port
EXPOSE 4000
# Set the entrypoint to run the Rails server
CMD ["rails", "server", "-b", "0.0.0.0"]
