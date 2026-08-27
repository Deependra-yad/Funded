with open("app/templates/admin_dashboard.html", "r", encoding="utf-8") as f:
    html = f.read()

if "onchange=\"loadDynamicPage()\"" not in html:
    html = html.replace("<select id=\"content-page-select\"", "<select id=\"content-page-select\" onchange=\"loadDynamicPage()\"")
    with open("app/templates/admin_dashboard.html", "w", encoding="utf-8") as f:
        f.write(html)
print("Select bound")
