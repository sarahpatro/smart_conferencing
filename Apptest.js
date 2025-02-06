import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders navbar brand", () => {
  render(<App />);
  const brandElement = screen.getByText(/MeetGenius AI/i);
  expect(brandElement).toBeInTheDocument();
});

test("renders home page by default", () => {
  render(<App />);
  const homeElement = screen.getByText(/Revolutionizing office meetings/i);
  expect(homeElement).toBeInTheDocument();
});
