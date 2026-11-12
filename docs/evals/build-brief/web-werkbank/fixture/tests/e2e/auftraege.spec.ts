import { test, expect } from "@playwright/test";

test("Übersicht zeigt Aufträge", async ({ page }) => {
  await page.goto("http://localhost:3100/auftraege");
  await expect(page.getByRole("heading", { name: "Aufträge" })).toBeVisible();
});
