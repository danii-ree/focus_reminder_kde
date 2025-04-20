# Focus Reminder

A smart screen monitoring application that helps you stay focused by detecting distracting content and providing gentle reminders.

## Features

- **Smart Screen Monitoring**: Uses OCR technology to analyze your screen content in real-time
- **Progressive Timeouts**: Each distraction increases the timeout period, encouraging better focus habits
- **Focus Reinforcement**: Provides gentle reminders when distractions are detected
- **Progress Tracking**: Keeps track of your distraction patterns
- **System Service**: Runs as a background service on KDE machines
- **Beautiful UI**: Clean, modern interface with smooth animations

## Requirements

- Python 3.x
- Tesseract OCR
- KDE Plasma desktop environment
- spectacle (KDE screenshot tool)

## Installation

1. Install required system packages:
```bash
sudo pacman -S tesseract tesseract-data-eng spectacle
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install the systemd service:
```bash
chmod +x install_service.sh
./install_service.sh
```

## Usage

The service will automatically start and run in the background. When distracting content is detected, a focus reminder will appear.

### Managing the Service

- Check status: `systemctl status focus_reminder.service`
- Stop service: `systemctl stop focus_reminder.service`
- Start service: `systemctl start focus_reminder.service`
- Disable auto-start: `systemctl disable focus_reminder.service`
- View logs: `journalctl -u focus_reminder.service`

## Configuration

- Edit `keywords.txt` to customize the distraction keywords
- The service logs are stored in `focus_reminder.log`

### Customizing Keywords

The `keywords.txt` file contains a list of words and phrases that the application will detect as distractions. Each keyword should be on a new line. The application will match these keywords case-insensitively.

Example `keywords.txt`:
```
gaming
entertainment
funny
comedy
music
social media
```

Tips for effective keyword configuration:
- Use specific terms relevant to your distractions
- Include variations of words (e.g., "game", "gaming", "gamer")
- Add common website names you want to avoid
- Keep the list focused - too many keywords may cause false positives
- Test new keywords by running the service and checking the logs

To apply changes to keywords:
1. Edit the `keywords.txt` file
2. Restart the service: `systemctl restart focus_reminder.service`

## Security

- The application runs locally and doesn't send any data to external servers
- Screen captures are processed locally and immediately deleted
- No personal data is stored or transmitted
