# DeepResearch Pipeline Frontend

A modern React TypeScript application built with Chakra UI for interacting with the DeepResearch pipeline.

## Features

- 🎨 Modern, responsive UI built with Chakra UI
- ⚡ TypeScript for type safety
- 🔄 Real-time pipeline status tracking
- 📱 Mobile-friendly responsive design
- 🎯 Clean, intuitive user experience
- 🔔 Toast notifications for user feedback
- 📊 Progress tracking with loading states

## Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

3. **Open your browser:**
   Navigate to `http://localhost:3000`

## Usage

1. **Enter a Research Query:** Type your research prompt in the textarea
2. **Start Research:** Click the "Start Research" button to kick off the pipeline
3. **Monitor Progress:** Watch real-time status updates as your query is processed
4. **View Results:** See completed results displayed in the results section

## API Integration

Currently, the application uses mock data for demonstration. To connect it to your backend:

1. Replace the placeholder code in the `handleSubmit` function in `src/App.tsx`
2. Update the API endpoint to match your backend URL
3. Modify the result handling logic based on your API response format

Example integration:
```typescript
// Replace the setTimeout simulation with actual API call
const response = await fetch('/api/research', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ prompt }),
});

const data = await response.json();
```

## Project Structure

```
src/
├── App.tsx           # Main application component
├── index.tsx         # Entry point with ChakraProvider
├── App.test.tsx      # Tests
└── ...
```

## Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

## Technologies Used

- **React 19** - Frontend framework
- **TypeScript** - Type safety
- **Chakra UI** - Component library
- **Emotion** - CSS-in-JS styling
- **Framer Motion** - Animations

## Customization

The application is built with Chakra UI, making it easy to customize:

- **Colors:** Modify the color scheme in the component props
- **Layout:** Adjust container sizes and spacing
- **Theme:** Add a custom Chakra UI theme
- **Components:** Extend or replace existing components

## Backend Integration Notes

When integrating with your backend, ensure:

1. **CORS:** Configure your backend to allow frontend requests
2. **Error Handling:** Implement proper error responses
3. **Status Updates:** Consider WebSocket or polling for real-time updates
4. **Authentication:** Add authentication if required

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the A2A DeepResearch system.
