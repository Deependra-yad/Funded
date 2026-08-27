# Implementation Plan: Final Production Fixes

## Goal
Fix responsive design issues, certificate printing, permanent notifications, fund/payout logic, account deletion flow, and terminal chart issues before production launch.

## Proposed Changes

### 1. Dashboard Responsiveness
#### [MODIFY] `app/templates/dashboard.html`
- Update the layout grid (`grid-cols-1 md:grid-cols-4`, etc.) to stack cards on mobile and allow sideways scrolling or wrapping. 
- Ensure Sidebar is accessible on mobile or hidden intelligently.
- Fix overlapping text classes (e.g. `truncate` or `text-wrap`).

### 2. Certificate Printing & Admin Customization
#### [MODIFY] `app/templates/certificate_detail.html`
- Add a `<style>` block with `@media print` to hide the sidebar, header, and print buttons. Ensure only the certificate frame is printed.
#### [NEW] `app/models.py` (AppSetting Model)
- Add `AppSetting` model to store the `managing_director_name`.
#### [MODIFY] `app/routers/certificates.py`
- Query the `AppSetting` to dynamically pass the director's name to the template.

### 3. Permanent Notifications & Advanced Broadcast
#### [MODIFY] `app/routers/admin_dashboard.py`
- Update `admin_generic_action` to handle a `message` text parameter for broadcasting custom text.
#### [MODIFY] `app/templates/admin_dashboard.html`
- Add a text input field in a modal for broadcasting custom messages, rather than a generic button.
#### [MODIFY] `app/templates/dashboard.html`
- Add an 'x' (dismiss) button to notifications in the UI.
#### [MODIFY] `app/routers/dashboard.py`
- Add an endpoint `/api/notifications/{id}/dismiss` to set `is_read=True` (or delete it from DB).

### 4. Admin Fund User Button
#### [MODIFY] `app/templates/admin_dashboard.html`
- Ensure there is a "Fund Account" button for accounts in Phase 2.
#### [MODIFY] `app/routers/admin_dashboard.py`
- Update account actions to handle "Fund" (move account to "Funded" phase, reset equity, and remove targets).

### 5. Deletion Request Flow with Reason
#### [MODIFY] `app/models.py` & `app/main.py`
- Add `deletion_reason` to `User` model. Update `main.py` startup raw SQL to add `deletion_reason` column safely on PostgreSQL.
#### [MODIFY] `app/routers/auth.py`
- Update `/profile/delete-request` to accept `reason` from the form.
#### [MODIFY] `app/templates/profile.html`
- Add a textarea for the reason in the danger zone.
#### [MODIFY] `app/templates/admin_dashboard.html`
- Show the deletion reason in the admin panel so the admin knows why they are deleting.

### 6. Terminal Chart Fixes
#### [MODIFY] `app/templates/trading_terminal.html`
- Check why TradingView chart dragging isn't working (likely pointer events issues or `div` overlaying the chart).
- Update Option Chain to sync the selected strike price to the main chart using TradingView API or `postMessage`.

## Verification Plan
- Launch the backend.
- Open `/dashboard` on a small screen (mobile view in dev tools) to verify responsiveness.
- Print the certificate page and verify the layout.
- Open `/terminal` and drag the chart, select an option chain strike, and verify it updates the TV chart.
- Verify the admin can change the certificate name and broadcast custom messages.
