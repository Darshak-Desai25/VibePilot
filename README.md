VibePilot

VibePilot is a lightweight automation tool that streamlines social media workflows—batch-scheduling posts, automating routine engagement, and managing multiple accounts from one place. Save time, stay consistent, and grow your presence without manual grind.

Features
- Automated Posting: Queue, schedule, and auto-publish content to supported platforms.
- Smart Engagement: Optional like/comment actions driven by simple, customizable rules.
- Multi-Account / Multi-Platform: Manage several profiles from a single interface.
- Easy Configuration: Minimal setup via config file or environment variables.
- Extensible: Modular adapters make it easy to add new platforms or actions.

Tech Stack
- Language: Python 3.8+
- Core: requests, scheduling libs (e.g., APScheduler), logging
- Structure: Pluggable “platform adapters” + rule-based engagement engine

Getting Started
- Prerequisites
  Python 3.8+

Required libraries (see requirements.txt)

- Installation

# clone your fork or the original repo
git clone https://github.com/Vaibhav5550/Auto-social-vibe.git
cd "path to your project"

# install dependencies
pip install -r requirements.txt
- Configuration
  Create a .env or edit config.yaml with your credentials and preferences.
  Example .env:
ini
Copy
Edit
PLATFORM=twitter
TW_API_KEY=...
TW_API_SECRET=...
POST_SCHEDULE_CRON=*/15 * * * *   # every 15 minutes (example)
ENGAGE_RULES_PATH=rules.yaml

- Example config.yaml:

yaml
Copy
Edit
platforms:
  - name: twitter
    credentials:
      api_key: YOUR_KEY
      api_secret: YOUR_SECRET
    posting:
      timezone: "Asia/Kolkata"
      schedule:
        - "0 9 * * 1-5"     # weekdays 9:00
        - "30 18 * * 1-5"   # weekdays 18:30
    engagement:
      like:
        hashtags: ["#ai", "#python"]
        max_per_hour: 10
      comment:
        templates: ["Love this!", "Great insights!", "🔥"]
        max_per_hour: 3
  Run
  python main.py

  Usage
 - Add posts to your content queue (CSV/JSON or UI if provided).
 - Tune schedules and engagement rules in config.yaml or .env.
 - Monitor logs for actions taken and adjust rate limits to stay compliant.

  Extending
- Implement a new adapter in adapters/<platform>.py with methods:
authenticate()
post(content)
like(criteria)
comment(criteria, template)

- Register your adapter in the factory and add config entries—done.

Roadmap (suggested)
- Web dashboard (Next.js) for queues, calendars, and logs
- Template variables (e.g., {day}, {hashtag}) and A/B post testing
- Native retry/backoff + platform-specific rate-limit handling
- Built-in content calendar import (CSV/Notion/Google Sheets)

