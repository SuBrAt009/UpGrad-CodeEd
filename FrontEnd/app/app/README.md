# upGrad Login Page

A modern, responsive login/signup page built with React and CSS, designed to match the upGrad brand aesthetic.

## Features

- Clean, minimalist design with upGrad branding
- Responsive layout that works on all devices
- Interactive form with User ID and Password fields
- Animated rocket illustration
- Smooth hover effects and transitions
- Accessible form design

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Design Details

The page features:
- **Logo**: "upGrad" in the signature red color (#E63946)
- **Form**: Two input fields with rounded corners and subtle shadows
- **Button**: Red "Next" button with hover effects
- **Illustration**: Animated rocket with a person inside, positioned on the left side
- **Colors**: Clean white background with red accents matching the upGrad brand

## File Structure

```
src/
├── App.js          # Main React component
├── App.css         # Styles for the login page
└── index.js        # React app entry point
public/
└── index.html      # HTML template
```

## Customization

You can easily customize:
- Colors by modifying the CSS variables in `App.css`
- Form validation by adding logic to the `handleSubmit` function
- Styling by updating the CSS classes
- Content by modifying the JSX in `App.js`
