/** Theme context + provider with high-contrast toggle. */
import React, { createContext, useContext, useMemo, useState } from "react";
import { type Theme, lightTheme, highContrastTheme } from "./tokens";

interface ThemeContextValue {
  theme: Theme;
  highContrast: boolean;
  toggleHighContrast: () => void;
}

const ThemeContext = createContext<ThemeContextValue>({
  theme: lightTheme,
  highContrast: false,
  toggleHighContrast: () => {},
});

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [highContrast, setHighContrast] = useState(false);
  const value = useMemo<ThemeContextValue>(
    () => ({
      theme: highContrast ? highContrastTheme : lightTheme,
      highContrast,
      toggleHighContrast: () => setHighContrast((v) => !v),
    }),
    [highContrast]
  );
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme(): ThemeContextValue {
  return useContext(ThemeContext);
}
