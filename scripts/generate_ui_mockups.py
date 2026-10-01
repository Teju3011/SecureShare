"""
SecureShare - Automated UI Mockup Graphics Generator
Generates high-resolution mockup visuals for artifacts/ui/:
- Login.png
- Dashboard.png
- Upload.png
- Quarantine.png
- Audit_Logs.png
- Permissions.png
- Demo_Dashboard.png
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

UI_DIR = os.path.join(os.path.dirname(__file__), "..", "artifacts", "ui")
os.makedirs(UI_DIR, exist_ok=True)

def draw_window_frame(ax, title):
    # Browser window chrome
    chrome = patches.FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.01",
                                    facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.5)
    ax.add_patch(chrome)
    
    # Header bar
    hbar = patches.Rectangle((0.02, 0.91), 0.96, 0.07, facecolor="#0F172A")
    ax.add_patch(hbar)
    
    # Window dots
    ax.plot([0.05, 0.07, 0.09], [0.945, 0.945, 0.945], 'o', color="#EF4444", markersize=6)
    
    # Brand logo & title
    ax.text(0.13, 0.945, f"🛡️ SECURESHARE — {title}", ha='left', va='center',
            fontsize=10.5, fontweight='bold', color='#FFFFFF')
    ax.text(0.85, 0.945, "👤 Sushmitha Reddy (Lead)", ha='center', va='center',
            fontsize=8.5, color='#94A3B8')

# 1. Login Mockup
def make_login_mockup():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=250)
    ax.axis('off')
    draw_window_frame(ax, "User Authentication & MFA")
    
    # Login Card
    card = patches.FancyBboxPatch((0.28, 0.15), 0.44, 0.68, boxstyle="round,pad=0.02",
                                  facecolor="#FFFFFF", edgecolor="#E2E8F0", linewidth=1.5)
    ax.add_patch(card)
    
    ax.text(0.50, 0.74, "Sign In to SecureShare", ha='center', va='center',
            fontsize=14, fontweight='bold', color='#0F172A')
    ax.text(0.50, 0.69, "Zero-Trust Enterprise File Security", ha='center', va='center',
            fontsize=9, color='#64748B')
            
    # Input fields
    for y, label, val in [(0.58, "Work Email", "sushmitha@example.com"),
                          (0.46, "Master Password", "••••••••••••••••")]:
        ax.text(0.33, y + 0.04, label, fontsize=8.5, fontweight='bold', color='#334155')
        box = patches.Rectangle((0.33, y - 0.02), 0.34, 0.05, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=1)
        ax.add_patch(box)
        ax.text(0.34, y + 0.005, val, fontsize=8, color='#0F172A')
        
    # Sign in Button
    btn = patches.FancyBboxPatch((0.33, 0.32), 0.34, 0.06, boxstyle="round,pad=0.01",
                                facecolor="#4F46E5", edgecolor="#4338CA", lw=1)
    ax.add_patch(btn)
    ax.text(0.50, 0.35, "Sign In with MFA →", ha='center', va='center',
            fontsize=10, fontweight='bold', color='#FFFFFF')
            
    # Quick switch badges
    ax.text(0.50, 0.24, "⚡ Quick 1-Click Grading Login:", ha='center', fontsize=8, color='#64748B')
    badges = ["Sushmitha (Owner)", "Rahul (Crypto)", "Admin (SOC)", "Auditor"]
    for i, b in enumerate(badges):
        bx = 0.31 + (i * 0.10)
        pill = patches.Rectangle((bx - 0.03, 0.17), 0.08, 0.035, facecolor="#EEF2FF", edgecolor="#C7D2FE", lw=0.8)
        ax.add_patch(pill)
        ax.text(bx + 0.01, 0.187, b.split()[0], ha='center', va='center', fontsize=6.5, color='#4338CA', fontweight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(UI_DIR, "Login.png"), bbox_inches='tight')
    plt.close(fig)

# 2. Dashboard Mockup
def make_dashboard_mockup():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=250)
    ax.axis('off')
    draw_window_frame(ax, "Security Dashboard & Telemetry")
    
    # 4 Metric Cards
    cards = [
        ("Total Files", "4 Files", "100% Encrypted", "#EEF2FF", "#4338CA"),
        ("Storage At Rest", "6.2 MB", "AES-256-GCM", "#ECFDF5", "#059669"),
        ("Active Shares", "3 Links", "2 Password Protected", "#FEF3C7", "#D97706"),
        ("Security Score", "98 / 100", "Zero Unmitigated Vulns", "#F0FDF4", "#16A34A")
    ]
    for i, (t, v, sub, bg, border) in enumerate(cards):
        cx = 0.06 + (i * 0.22)
        box = patches.FancyBboxPatch((cx, 0.68), 0.20, 0.18, boxstyle="round,pad=0.01",
                                    facecolor=bg, edgecolor=border, lw=1.2)
        ax.add_patch(box)
        ax.text(cx + 0.02, 0.82, t, fontsize=8.5, fontweight='bold', color='#475569')
        ax.text(cx + 0.02, 0.76, v, fontsize=14, fontweight='bold', color=border)
        ax.text(cx + 0.02, 0.71, sub, fontsize=7.5, color='#64748B')
        
    # Recent Files Table
    tbl = patches.FancyBboxPatch((0.06, 0.10), 0.86, 0.52, boxstyle="round,pad=0.01",
                                facecolor="#FFFFFF", edgecolor="#E2E8F0", lw=1.2)
    ax.add_patch(tbl)
    ax.text(0.09, 0.58, "Recent Secure Files & Verification Status", fontsize=10.5, fontweight='bold', color='#0F172A')
    
    # Table headers
    th = patches.Rectangle((0.08, 0.51), 0.82, 0.04, facecolor="#F1F5F9")
    ax.add_patch(th)
    ax.text(0.10, 0.53, "FILENAME", fontsize=7.5, fontweight='bold', color='#475569')
    ax.text(0.38, 0.53, "ENCRYPTION", fontsize=7.5, fontweight='bold', color='#475569')
    ax.text(0.58, 0.53, "SCAN RESULT", fontsize=7.5, fontweight='bold', color='#475569')
    ax.text(0.78, 0.53, "ACTIONS", fontsize=7.5, fontweight='bold', color='#475569')
    
    rows = [
        ("Security_Report.pdf", "AES-256-GCM (128-bit tag)", "✅ CLEAN", "Download  |  Share"),
        ("SecureShare_SRS.docx", "AES-256-GCM (128-bit tag)", "✅ CLEAN", "Download  |  Share"),
        ("Architecture_Diagram.png", "AES-256-GCM (128-bit tag)", "✅ CLEAN", "Download  |  Share"),
        ("eicar_test_sample.com", "Quarantined (Air-gapped)", "⛔ INFECTED", "View Alert  |  Purge")
    ]
    for idx, (f, enc, sc, act) in enumerate(rows):
        ry = 0.44 - (idx * 0.08)
        c_status = '#16A34A' if 'CLEAN' in sc else '#DC2626'
        ax.text(0.10, ry, f, fontsize=8, fontweight='bold', color='#1E293B')
        ax.text(0.38, ry, enc, fontsize=7.5, color='#475569')
        ax.text(0.58, ry, sc, fontsize=7.5, fontweight='bold', color=c_status)
        ax.text(0.78, ry, act, fontsize=7.5, color='#4F46E5', fontweight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(UI_DIR, "Dashboard.png"), bbox_inches='tight')
    plt.close(fig)

# 3. Upload Mockup
def make_upload_mockup():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=250)
    ax.axis('off')
    draw_window_frame(ax, "Secure File Upload & 6-Stage Scanner")
    
    # Drag-and-drop zone
    drop = patches.FancyBboxPatch((0.08, 0.52), 0.84, 0.34, boxstyle="round,pad=0.01",
                                 facecolor="#EEF2FF", edgecolor="#6366F1", lw=2, linestyle="--")
    ax.add_patch(drop)
    ax.text(0.50, 0.74, "📁 Drag & Drop Confidential Files Here", ha='center', fontsize=13, fontweight='bold', color='#4338CA')
    ax.text(0.50, 0.67, "Supported formats: PDF, DOCX, XLSX, PNG, JPG, ZIP (Max 50MB)", ha='center', fontsize=8.5, color='#64748B')
    ax.text(0.50, 0.60, "Files automatically undergo 6-stage malware scanning & AES-256 envelope encryption", ha='center', fontsize=8, color='#4F46E5')
    
    # 6-Stage Scanner Visualizer Card
    scan_card = patches.FancyBboxPatch((0.08, 0.10), 0.84, 0.38, boxstyle="round,pad=0.01",
                                       facecolor="#FFFFFF", edgecolor="#E2E8F0", lw=1.2)
    ax.add_patch(scan_card)
    ax.text(0.11, 0.43, "Real-Time 6-Stage Threat Scanning Pipeline", fontsize=10.5, fontweight='bold', color='#0F172A')
    
    stages = [
        ("1. Size (<50MB)", "PASSED", "#16A34A"),
        ("2. MIME Magic", "PASSED", "#16A34A"),
        ("3. PE Header", "PASSED", "#16A34A"),
        ("4. Zip Bomb", "PASSED", "#16A34A"),
        ("5. ClamAV", "SCANNING...", "#F59E0B"),
        ("6. Entropy", "QUEUED", "#94A3B8")
    ]
    for idx, (sname, st, sc) in enumerate(stages):
        sx = 0.11 + (idx * 0.13)
        p = patches.Rectangle((sx, 0.22), 0.11, 0.14, facecolor="#F8FAFC", edgecolor=sc, lw=1.2)
        ax.add_patch(p)
        ax.text(sx + 0.055, 0.31, sname, ha='center', fontsize=6.8, fontweight='bold', color='#1E293B')
        ax.text(sx + 0.055, 0.25, st, ha='center', fontsize=6.5, fontweight='bold', color=sc)

    plt.tight_layout()
    fig.savefig(os.path.join(UI_DIR, "Upload.png"), bbox_inches='tight')
    plt.close(fig)

# 4. Quarantine Mockup
def make_quarantine_mockup():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=250)
    ax.axis('off')
    draw_window_frame(ax, "SOC Admin Quarantine Isolation Center")
    
    # Alert banner
    ban = patches.FancyBboxPatch((0.06, 0.78), 0.88, 0.09, boxstyle="round,pad=0.01",
                                 facecolor="#FEF2F2", edgecolor="#EF4444", lw=1.2)
    ax.add_patch(ban)
    ax.text(0.08, 0.83, "🚨 Active Quarantine Isolation Enforced", fontsize=10, fontweight='bold', color='#B91C1C')
    ax.text(0.08, 0.80, "Files flagged as high-risk or malicious are air-gapped on isolated storage volumes. Downloads return HTTP 403 Forbidden.", fontsize=7.5, color='#7F1D1D')
    
    # Quarantine table
    qtbl = patches.FancyBboxPatch((0.06, 0.10), 0.88, 0.64, boxstyle="round,pad=0.01",
                                  facecolor="#FFFFFF", edgecolor="#E2E8F0", lw=1.2)
    ax.add_patch(qtbl)
    
    th = patches.Rectangle((0.08, 0.67), 0.84, 0.04, facecolor="#F8FAFC")
    ax.add_patch(th)
    ax.text(0.10, 0.69, "QUARANTINED ARTIFACT", fontsize=7.5, fontweight='bold', color='#475569')
    ax.text(0.35, 0.69, "THREAT DETECTED", fontsize=7.5, fontweight='bold', color='#475569')
    ax.text(0.60, 0.69, "STAGE DETECTED", fontsize=7.5, fontweight='bold', color='#475569')
    ax.text(0.78, 0.69, "ADMIN ACTION", fontsize=7.5, fontweight='bold', color='#475569')
    
    qrows = [
        ("eicar_test_sample.com", "EICAR Standard Antivirus Test", "Stage 5 (ClamAV)", "Release  |  [PURGE]"),
        ("invoice_payload.pdf.exe", "Windows PE Executable Disguised", "Stage 2 (MIME Magic)", "Release  |  [PURGE]"),
        ("macro_exploit.docm", "Embedded VBA AutoExec Macro", "Stage 3 (Header Scan)", "Release  |  [PURGE]"),
        ("archive_bomb_100gb.zip", "High Compression Zip Bomb Ratio", "Stage 4 (Archive Check)", "Release  |  [PURGE]")
    ]
    for idx, (f, thrt, stg, act) in enumerate(qrows):
        qy = 0.58 - (idx * 0.11)
        ax.text(0.10, qy, f, fontsize=8, fontweight='bold', color='#B91C1C')
        ax.text(0.35, qy, thrt, fontsize=7.5, color='#475569')
        ax.text(0.60, qy, stg, fontsize=7.5, fontweight='bold', color='#D97706')
        ax.text(0.78, qy, act, fontsize=7.5, color='#DC2626', fontweight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(UI_DIR, "Quarantine.png"), bbox_inches='tight')
    plt.close(fig)

# 5. Audit Logs Mockup
def make_audit_mockup():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=250)
    ax.axis('off')
    draw_window_frame(ax, "Tamper-Evident SHA-256 Audit Trail")
    
    # Verifier Status Box
    vbox = patches.FancyBboxPatch((0.06, 0.78), 0.88, 0.09, boxstyle="round,pad=0.01",
                                  facecolor="#F0FDF4", edgecolor="#16A34A", lw=1.2)
    ax.add_patch(vbox)
    ax.text(0.08, 0.83, "🛡️ Blockchain Audit Ledger Integrity: VERIFIED (100% Valid)", fontsize=10, fontweight='bold', color='#15803D')
    ax.text(0.08, 0.80, "All 42 audit log rows form an unbroken cryptographic SHA-256 hash chain. Zero row tampering or deletion detected.", fontsize=7.5, color='#166534')
    
    # Audit table
    atbl = patches.FancyBboxPatch((0.06, 0.10), 0.88, 0.64, boxstyle="round,pad=0.01",
                                  facecolor="#FFFFFF", edgecolor="#E2E8F0", lw=1.2)
    ax.add_patch(atbl)
    
    th = patches.Rectangle((0.08, 0.67), 0.84, 0.04, facecolor="#F8FAFC")
    ax.add_patch(th)
    ax.text(0.10, 0.69, "TIMESTAMP", fontsize=7.5, fontweight='bold', color='#475569')
    ax.text(0.24, 0.69, "ACTOR", fontsize=7.5, fontweight='bold', color='#475569')
    ax.text(0.42, 0.69, "ACTION", fontsize=7.5, fontweight='bold', color='#475569')
    ax.text(0.60, 0.69, "IP ADDRESS", fontsize=7.5, fontweight='bold', color='#475569')
    ax.text(0.74, 0.69, "SHA-256 BLOCK HASH", fontsize=7.5, fontweight='bold', color='#475569')
    
    arows = [
        ("10:04:12", "sushmitha@example.com", "FILE_UPLOAD_CLEAN", "192.168.1.104", "a4f89d...1e8b (Valid)"),
        ("10:02:45", "rahul@example.com", "FILE_DOWNLOADED", "192.168.1.108", "c381ef...4401 (Valid)"),
        ("09:58:30", "admin@example.com", "AUDIT_VERIFIED", "127.0.0.1", "b211a7...9923 (Valid)"),
        ("09:55:12", "attacker@unknown.net", "USER_LOGIN_FAILURE", "45.33.32.156", "771eac...8120 (Valid)")
    ]
    for idx, (ts, act, actn, ip, hsh) in enumerate(arows):
        ay = 0.58 - (idx * 0.11)
        ax.text(0.10, ay, ts, fontsize=7.5, color='#64748B')
        ax.text(0.24, ay, act, fontsize=7.5, fontweight='bold', color='#1E293B')
        ax.text(0.42, ay, actn, fontsize=7.5, fontweight='bold', color='#4338CA')
        ax.text(0.60, ay, ip, fontsize=7.5, color='#475569')
        ax.text(0.74, ay, hsh, fontsize=7.2, color='#15803D', fontfamily='monospace')

    plt.tight_layout()
    fig.savefig(os.path.join(UI_DIR, "Audit_Logs.png"), bbox_inches='tight')
    plt.close(fig)

# 6. Permissions Mockup
def make_permissions_mockup():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=250)
    ax.axis('off')
    draw_window_frame(ax, "Granular File Access Control (DAC)")
    
    card = patches.FancyBboxPatch((0.15, 0.12), 0.70, 0.74, boxstyle="round,pad=0.01",
                                  facecolor="#FFFFFF", edgecolor="#E2E8F0", lw=1.5)
    ax.add_patch(card)
    
    ax.text(0.18, 0.81, "Manage Permissions for: Security_Report.pdf", fontsize=11, fontweight='bold', color='#0F172A')
    ax.text(0.18, 0.77, "Grant granular access without exposing root master keys.", fontsize=8, color='#64748B')
    
    # Form
    ax.text(0.18, 0.70, "Add Collaborator Email:", fontsize=8.5, fontweight='bold', color='#334155')
    inp = patches.Rectangle((0.18, 0.63), 0.38, 0.05, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=1)
    ax.add_patch(inp)
    ax.text(0.20, 0.655, "rahul@example.com", fontsize=8, color='#0F172A')
    
    # Preset Selector
    ax.text(0.58, 0.70, "Role Preset:", fontsize=8.5, fontweight='bold', color='#334155')
    sel = patches.Rectangle((0.58, 0.63), 0.22, 0.05, facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=1)
    ax.add_patch(sel)
    ax.text(0.60, 0.655, "DOWNLOADER ▾", fontsize=8, fontweight='bold', color='#4F46E5')
    
    # Existing Access Table
    th = patches.Rectangle((0.18, 0.50), 0.64, 0.04, facecolor="#F1F5F9")
    ax.add_patch(th)
    ax.text(0.20, 0.52, "USER EMAIL", fontsize=7.5, fontweight='bold', color='#475569')
    ax.text(0.48, 0.52, "ROLE PRESET", fontsize=7.5, fontweight='bold', color='#475569')
    ax.text(0.68, 0.52, "STATUS / ACTION", fontsize=7.5, fontweight='bold', color='#475569')
    
    prows = [
        ("sushmitha@example.com", "OWNER (Full Control)", "Primary Owner"),
        ("rahul@example.com", "DOWNLOADER", "Active  |  [Revoke]"),
        ("priya@example.com", "VIEWER (Read Only)", "Active  |  [Revoke]")
    ]
    for idx, (em, rle, act) in enumerate(prows):
        py = 0.43 - (idx * 0.09)
        ax.text(0.20, py, em, fontsize=8, color='#1E293B')
        ax.text(0.48, py, rle, fontsize=7.5, fontweight='bold', color='#4338CA')
        ax.text(0.68, py, act, fontsize=7.5, color='#DC2626' if 'Revoke' in act else '#64748B', fontweight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(UI_DIR, "Permissions.png"), bbox_inches='tight')
    plt.close(fig)

# 7. Demo Dashboard Mockup
def make_demo_dashboard_mockup():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=250)
    ax.axis('off')
    draw_window_frame(ax, "Live Evaluation & Course Review Dashboard (/demo)")
    
    # Header Banner
    hban = patches.FancyBboxPatch((0.05, 0.77), 0.90, 0.10, boxstyle="round,pad=0.01",
                                  facecolor="#0F172A", edgecolor="#334155", lw=1.2)
    ax.add_patch(hban)
    ax.text(0.08, 0.83, "🎓 College Capstone Demonstration Center — SecureShare v1.0", fontsize=11, fontweight='bold', color='#FFFFFF')
    ax.text(0.08, 0.80, "Interactive presentation panel for examiners: live metrics, 6 persona switches, and continuous security telemetry.", fontsize=7.5, color='#94A3B8')
    
    # 8 Summary Cards Grid
    metrics = [
        ("Active Users", "6 Personas", "#EEF2FF", "#4338CA"),
        ("Clean Files", "4 Encrypted", "#ECFDF5", "#059669"),
        ("Quarantine Vault", "1 Malware Sample", "#FEF2F2", "#DC2626"),
        ("Audit Chain", "100% Tamper-Proof", "#F0FDF4", "#16A34A"),
        ("CI/CD Pipeline", "Pass (Gate Green)", "#EFF6FF", "#2563EB"),
        ("Security Tests", "48 / 48 Passed", "#FDF2F8", "#BE185D"),
        ("Vulnerabilities", "0 Critical / High", "#F5F3FF", "#7C3AED"),
        ("IEEE 29148", "Compliant", "#FEF3C7", "#D97706")
    ]
    for i, (lbl, val, bg, border) in enumerate(metrics):
        col = i % 4
        row = i // 4
        gx = 0.05 + (col * 0.23)
        gy = 0.58 - (row * 0.14)
        box = patches.FancyBboxPatch((gx, gy), 0.21, 0.12, boxstyle="round,pad=0.005",
                                     facecolor=bg, edgecolor=border, lw=1)
        ax.add_patch(box)
        ax.text(gx + 0.015, gy + 0.08, lbl, fontsize=7.2, fontweight='bold', color='#475569')
        ax.text(gx + 0.015, gy + 0.035, val, fontsize=9.5, fontweight='bold', color=border)

    # 1-Click Evaluation Switcher
    pbox = patches.FancyBboxPatch((0.05, 0.10), 0.90, 0.16, boxstyle="round,pad=0.01",
                                  facecolor="#FFFFFF", edgecolor="#CBD5E1", lw=1.2)
    ax.add_patch(pbox)
    ax.text(0.08, 0.22, "1-Click Examiner Persona Switcher (Simulates Complete Enterprise Roles):", fontsize=8.5, fontweight='bold', color='#0F172A')
    
    pbuttons = [
        ("Sushmitha (Lead)", "#4F46E5"), ("Rahul (Crypto)", "#4F46E5"),
        ("Priya (DevSecOps)", "#4F46E5"), ("Arjun (UI/UX)", "#4F46E5"),
        ("Admin (SOC)", "#DC2626"), ("Auditor (Compliance)", "#059669")
    ]
    for idx, (pname, pcolor) in enumerate(pbuttons):
        bx = 0.08 + (idx * 0.14)
        btn = patches.Rectangle((bx, 0.13), 0.13, 0.06, facecolor=pcolor, edgecolor=pcolor)
        ax.add_patch(btn)
        ax.text(bx + 0.065, 0.16, pname, ha='center', va='center', fontsize=6.5, fontweight='bold', color='#FFFFFF')

    plt.tight_layout()
    fig.savefig(os.path.join(UI_DIR, "Demo_Dashboard.png"), bbox_inches='tight')
    plt.close(fig)

def main():
    print("[*] Generating UI Mockup PNG images in artifacts/ui/ ...")
    make_login_mockup()
    make_dashboard_mockup()
    make_upload_mockup()
    make_quarantine_mockup()
    make_audit_mockup()
    make_permissions_mockup()
    make_demo_dashboard_mockup()
    print("[+] Successfully generated all 7 UI mockup images!")

if __name__ == "__main__":
    main()
