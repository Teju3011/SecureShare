"""
SecureShare - Automated Architecture Diagrams & Charts Generator
Generates:
1. Architectural Diagrams (.drawio, .svg, .png):
   - Use_Case_Diagram
   - ER_Diagram
   - DFD_Level_0
   - DFD_Level_1
   - Trust_Boundary_Architecture
   - Attack_Tree
   - Secure_Architecture
2. Data Charts (.png, .svg):
   - Risk_Heat_Map.png
   - Burndown_Chart.png
   - Velocity_Chart.png
   - Sprint_Board.png
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "artifacts", "diagrams")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# Matplotlib High-Quality Theme Settings
# -------------------------------------------------------------
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

# -------------------------------------------------------------
# 1. 5x5 Risk Assessment Heat Map Chart
# -------------------------------------------------------------
def generate_risk_heatmap():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    
    # 5x5 matrix
    # Values: Impact (5 to 1, row 0 to 4) x Likelihood (1 to 5, col 0 to 4)
    matrix = np.array([
        [5, 10, 15, 20, 25],  # 5 - Catastrophic
        [4,  8, 12, 16, 20],  # 4 - Major
        [3,  6,  9, 12, 15],  # 3 - Moderate
        [2,  4,  6,  8, 10],  # 2 - Minor
        [1,  2,  3,  4,  5]   # 1 - Insignificant
    ])
    
    # Custom color map: Green -> Yellow -> Orange -> Red
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        'risk_cmap', ['#85E39C', '#FFEB9C', '#FFB380', '#FF6B6B']
    )
    
    cax = ax.imshow(matrix, cmap=cmap, aspect='auto', interpolation='nearest')
    
    # Labels
    impact_labels = ['5 - Catastrophic', '4 - Major', '3 - Moderate', '2 - Minor', '1 - Insignificant']
    likelihood_labels = ['1 - Rare', '2 - Unlikely', '3 - Moderate', '4 - Likely', '5 - Almost Certain']
    
    ax.set_yticks(np.arange(5))
    ax.set_yticklabels(impact_labels, fontsize=11, fontweight='bold', color='#1A2B4C')
    ax.set_xticks(np.arange(5))
    ax.set_xticklabels(likelihood_labels, fontsize=11, fontweight='bold', color='#1A2B4C')
    
    ax.set_ylabel('Impact Level', fontsize=13, fontweight='bold', color='#1F4E79', labelpad=12)
    ax.set_xlabel('Likelihood Level', fontsize=13, fontweight='bold', color='#1F4E79', labelpad=12)
    ax.set_title('SecureShare 5x5 Cyber Risk Assessment Matrix\nInherent vs Residual Risk Distribution', 
                 fontsize=14, fontweight='bold', color='#1F4E79', pad=18)
    
    # Cell text annotations
    annotations = [
        # Catastrophic
        ["5 (Low)\n[RSK-04*]", "10 (Med)", "15 (High)", "20 (Critical)\n[RSK-02, 03]", "25 (Critical)"],
        # Major
        ["4 (Low)\n[RSK-02*]", "8 (Med)\n[RSK-05]", "12 (High)\n[RSK-07, 08]", "16 (High)\n[RSK-01, 06]", "20 (Critical)"],
        # Moderate
        ["3 (Low)\n[RSK-01*, 07*]", "6 (Med)", "9 (Med)", "12 (High)", "15 (High)"],
        # Minor
        ["2 (Low)\n[RSK-05*, 06*, 08*]", "4 (Low)", "6 (Med)", "8 (Med)", "10 (Med)"],
        # Insignificant
        ["1 (Low)", "2 (Low)", "3 (Low)", "4 (Low)", "5 (Low)"]
    ]
    
    for i in range(5):
        for j in range(5):
            text = annotations[i][j]
            color = '#1A2B4C' if 'Critical' not in text else '#800000'
            ax.text(j, i, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color=color)
            
    # Grid lines
    ax.set_xticks(np.arange(-0.5, 5, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 5, 1), minor=True)
    ax.grid(which='minor', color='#FFFFFF', linestyle='-', linewidth=2.5)
    ax.tick_params(which='minor', size=0)
    
    # Legend note
    plt.figtext(0.5, 0.01, 
               "Legend: [RSK-XX] Inherent Pre-Mitigation Risk  |  [RSK-XX*] Residual Post-Mitigation Risk (All residual risks reduced to Low tier)",
               ha="center", fontsize=9, fontstyle="italic", color="#4A5568")
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    fig.savefig(os.path.join(OUTPUT_DIR, "Risk_Heat_Map.png"), bbox_inches='tight')
    fig.savefig(os.path.join(OUTPUT_DIR, "Risk_Heat_Map.svg"), bbox_inches='tight')
    plt.close(fig)

# -------------------------------------------------------------
# 2. Sprint Burndown Chart
# -------------------------------------------------------------
def generate_burndown_chart():
    days = np.arange(1, 11)
    
    # Sprint 1
    s1_ideal = np.linspace(36, 0, 10)
    s1_actual = [36, 34, 30, 26, 21, 18, 13, 9, 5, 0]
    
    # Sprint 2
    s2_ideal = np.linspace(38, 0, 10)
    s2_actual = [38, 35, 30, 26, 20, 16, 12, 8, 4, 0]
    
    # Sprint 3
    s3_ideal = np.linspace(40, 0, 10)
    s3_actual = [40, 36, 31, 26, 21, 17, 12, 8, 3, 0]
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5), dpi=300, sharey=False)
    
    sprints = [
        (ax1, "Sprint 1: Core Auth & Malware Scanner", s1_ideal, s1_actual, 36),
        (ax2, "Sprint 2: AES Cryptography & Audit Ledger", s2_ideal, s2_actual, 38),
        (ax3, "Sprint 3: DevSecOps CI/CD & Frontend UI", s3_ideal, s3_actual, 40)
    ]
    
    for ax, title, ideal, actual, max_pts in sprints:
        ax.plot(days, ideal, 'r--', label='Ideal Burndown', linewidth=2.2, alpha=0.85)
        ax.plot(days, actual, 'b-o', label='Actual Burndown', linewidth=2.5, markersize=6, color='#1F4E79')
        ax.fill_between(days, actual, alpha=0.12, color='#1F4E79')
        
        ax.set_title(title, fontsize=11, fontweight='bold', color='#1F4E79', pad=10)
        ax.set_xlabel('Sprint Working Day (Day 1 - 10)', fontsize=10, fontweight='bold')
        ax.set_ylabel('Story Points Remaining', fontsize=10, fontweight='bold')
        ax.set_xticks(days)
        ax.set_ylim(-1, max_pts + 5)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(loc='upper right', fontsize=9)
        
    fig.suptitle('SecureShare Scrum Delivery — Sprints 1, 2, and 3 Burndown Curves', 
                 fontsize=14, fontweight='bold', color='#1F4E79', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(os.path.join(OUTPUT_DIR, "Burndown_Chart.png"), bbox_inches='tight')
    fig.savefig(os.path.join(OUTPUT_DIR, "Burndown_Chart.svg"), bbox_inches='tight')
    plt.close(fig)

# -------------------------------------------------------------
# 3. Team Velocity Chart
# -------------------------------------------------------------
def generate_velocity_chart():
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
    
    sprints = ['Sprint 1\n(Auth & Scanner)', 'Sprint 2\n(Crypto & Sharing)', 'Sprint 3\n(DevSecOps & UI)']
    committed = [36, 38, 40]
    completed = [36, 38, 40]
    
    x = np.arange(len(sprints))
    width = 0.32
    
    rects1 = ax.bar(x - width/2, committed, width, label='Committed Points', color='#A0C4E2', edgecolor='#1F4E79', linewidth=1.2)
    rects2 = ax.bar(x + width/2, completed, width, label='Completed Points (100%)', color='#1F4E79', edgecolor='#0F2840', linewidth=1.2)
    
    ax.set_ylabel('Story Points', fontsize=11, fontweight='bold', color='#1F4E79')
    ax.set_title('SecureShare Engineering Velocity across Sprints\n100% Commitment Delivery (Zero Carryover)', 
                 fontsize=13, fontweight='bold', color='#1F4E79', pad=14)
    ax.set_xticks(x)
    ax.set_xticklabels(sprints, fontsize=10, fontweight='bold')
    ax.set_ylim(0, 48)
    ax.grid(axis='y', linestyle=':', alpha=0.6)
    ax.legend(fontsize=10)
    
    # Value labels
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f'{h} pts', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 4),
                    textcoords="offset points", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#1F4E79')
                    
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f'{h} pts', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 4),
                    textcoords="offset points", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#0F2840')

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "Velocity_Chart.png"), bbox_inches='tight')
    fig.savefig(os.path.join(OUTPUT_DIR, "Velocity_Chart.svg"), bbox_inches='tight')
    plt.close(fig)

# -------------------------------------------------------------
# 4. Sprint Scrum Board Graphic
# -------------------------------------------------------------
def generate_sprint_board():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    ax.axis('off')
    
    columns = [
        ("To Do (0)", 0.05, 0.25, "#F1F5F9", "#64748B"),
        ("In Progress (0)", 0.35, 0.25, "#FEF3C7", "#D97706"),
        ("In Review / Testing (0)", 0.65, 0.25, "#E0E7FF", "#4F46E5"),
        ("Done (18)", 0.95, 0.25, "#DCFCE7", "#16A34A")
    ]
    
    # Board Title
    ax.text(0.5, 0.95, "SecureShare Jira Scrum Board — Sprint 3 (Final Release)", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1F4E79')
    
    # Done items cards
    done_cards = [
        ("SEC-01", "Argon2id Password Hashing", "Rahul Kumar", "5 pts", "#E2E8F0"),
        ("SEC-04", "6-Stage Malware Scanner", "Priya Sharma", "8 pts", "#E2E8F0"),
        ("SEC-07", "AES-256-GCM Encryption", "Rahul Kumar", "8 pts", "#E2E8F0"),
        ("SEC-10", "DAC Granular Permissions", "Arjun Rao", "5 pts", "#E2E8F0"),
        ("SEC-12", "SHA-256 Audit Blockchain", "Sushmitha Reddy", "8 pts", "#E2E8F0"),
        ("SEC-15", "GitHub Actions CI/CD Gate", "Priya Sharma", "8 pts", "#E2E8F0"),
        ("SEC-17", "OWASP ZAP Baseline DAST", "Priya Sharma", "5 pts", "#E2E8F0"),
        ("SEC-14", "React Vite Glassmorphism UI", "Arjun Rao", "8 pts", "#E2E8F0")
    ]
    
    col_width = 0.22
    col_starts = [0.03, 0.27, 0.51, 0.75]
    
    for idx, (title, _, _, bg, border) in enumerate(columns):
        cx = col_starts[idx]
        rect = patches.FancyBboxPatch((cx, 0.05), col_width, 0.82, boxstyle="round,pad=0.01",
                                      facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(cx + col_width/2, 0.84, title, ha='center', va='center', 
                fontsize=11, fontweight='bold', color=border)
                
    # Place Done cards
    for c_idx, (key, summary, assignee, pts, cbg) in enumerate(done_cards):
        cy = 0.73 - (c_idx * 0.09)
        cx = col_starts[3] + 0.01
        card = patches.FancyBboxPatch((cx, cy), col_width - 0.02, 0.075, boxstyle="round,pad=0.005",
                                      facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.0)
        ax.add_patch(card)
        ax.text(cx + 0.01, cy + 0.05, f"{key}: {summary}", fontsize=8, fontweight='bold', color='#1E293B')
        ax.text(cx + 0.01, cy + 0.02, f"👤 {assignee}", fontsize=7.5, color='#64748B')
        ax.text(cx + col_width - 0.03, cy + 0.02, pts, fontsize=7.5, fontweight='bold', color='#16A34A', ha='right')

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "Sprint_Board.png"), bbox_inches='tight')
    fig.savefig(os.path.join(OUTPUT_DIR, "Sprint_Board.svg"), bbox_inches='tight')
    plt.close(fig)

# -------------------------------------------------------------
# 5. Architecture Diagrams Renderer (Matplotlib SVG + PNG)
# -------------------------------------------------------------
def render_box(ax, x, y, w, h, title, subtitle="", bg="#FFFFFF", border="#1F4E79", text_color="#1F4E79"):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                  facecolor=bg, edgecolor=border, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2 + (0.015 if subtitle else 0), title,
            ha='center', va='center', fontsize=9.5, fontweight='bold', color=text_color)
    if subtitle:
        ax.text(x + w/2, y + h/2 - 0.025, subtitle,
                ha='center', va='center', fontsize=7.5, color="#555555")

def render_arrow(ax, x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color="#1F4E79", lw=1.5, mutation_scale=12))
    if label:
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 0.015, label, ha='center', va='bottom', fontsize=7.5, 
                color="#0F2840", fontweight='bold', bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec="none", alpha=0.8))

# 5.1 Use Case Diagram
def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.axis('off')
    ax.set_title("SecureShare — IEEE 29148 Use Case Specification Diagram", 
                 fontsize=14, fontweight='bold', color='#1F4E79', pad=15)
    
    # Boundary Box (System Boundary)
    sys_rect = patches.FancyBboxPatch((0.26, 0.05), 0.52, 0.88, boxstyle="round,pad=0.02",
                                     facecolor="#F8FAFC", edgecolor="#1F4E79", linewidth=2.0)
    ax.add_patch(sys_rect)
    ax.text(0.52, 0.91, "SecureShare Application Boundary", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#1F4E79')
            
    # Actors (Left and Right)
    actors = [
        (0.08, 0.75, "👤 Regular User\n(File Owner / Consumer)"),
        (0.08, 0.40, "👤 Public Guest\n(Expiring Link Recipient)"),
        (0.92, 0.75, "🛡️ System Admin\n(SOC Operations)"),
        (0.92, 0.40, "📋 Security Auditor\n(Compliance Officer)")
    ]
    for x, y, text in actors:
        ax.text(x, y, text, ha='center', va='center', fontsize=9.5, fontweight='bold', 
                color='#0F2840', bbox=dict(boxstyle="round,pad=0.4", fc="#E2E8F0", ec="#64748B", lw=1.2))
                
    # Use Cases (Ovals in center)
    use_cases = [
        (0.38, 0.82, "UC-01: Argon2id Registration"),
        (0.64, 0.82, "UC-02: TOTP Multi-Factor Auth"),
        (0.38, 0.68, "UC-03: Multi-Stage Secure Upload"),
        (0.64, 0.68, "UC-04: 6-Stage Malware Scanner"),
        (0.38, 0.54, "UC-05: AES-256-GCM Encryption"),
        (0.64, 0.54, "UC-06: Authorized File Download"),
        (0.38, 0.40, "UC-07: Hierarchical Folder Guard"),
        (0.64, 0.40, "UC-08: Granular DAC Permissions"),
        (0.38, 0.26, "UC-09: Expiring Public Links"),
        (0.64, 0.26, "UC-10: SHA-256 Audit Verification"),
        (0.38, 0.12, "UC-11: Admin Quarantine Purge"),
        (0.64, 0.12, "UC-12: CI/CD DevSecOps Gate")
    ]
    
    for x, y, text in use_cases:
        ellipse = patches.Ellipse((x, y), 0.22, 0.08, facecolor="#FFFFFF", edgecolor="#1F4E79", linewidth=1.4)
        ax.add_patch(ellipse)
        ax.text(x, y, text, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#1E293B')
        
    # Association lines from Actors to Use Cases
    # Regular User
    ax.plot([0.15, 0.27], [0.75, 0.82], 'k-', lw=1.0, color="#64748B")
    ax.plot([0.15, 0.27], [0.75, 0.68], 'k-', lw=1.0, color="#64748B")
    ax.plot([0.15, 0.27], [0.75, 0.54], 'k-', lw=1.0, color="#64748B")
    ax.plot([0.15, 0.27], [0.75, 0.40], 'k-', lw=1.0, color="#64748B")
    # Public Guest
    ax.plot([0.15, 0.27], [0.40, 0.26], 'k-', lw=1.0, color="#64748B")
    ax.plot([0.15, 0.53], [0.40, 0.54], 'k-', lw=1.0, color="#64748B")
    # Admin
    ax.plot([0.85, 0.49], [0.75, 0.12], 'k-', lw=1.0, color="#64748B")
    ax.plot([0.85, 0.75], [0.75, 0.12], 'k-', lw=1.0, color="#64748B")
    ax.plot([0.85, 0.75], [0.75, 0.26], 'k-', lw=1.0, color="#64748B")
    # Auditor
    ax.plot([0.85, 0.75], [0.40, 0.26], 'k-', lw=1.0, color="#64748B")
    
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "Use_Case_Diagram.png"), bbox_inches='tight')
    fig.savefig(os.path.join(OUTPUT_DIR, "Use_Case_Diagram.svg"), bbox_inches='tight')
    plt.close(fig)

# 5.2 ER Diagram
def generate_er_diagram():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    ax.axis('off')
    ax.set_title("SecureShare — Entity-Relationship (ER) Schema Diagram", 
                 fontsize=14, fontweight='bold', color='#1F4E79', pad=15)
    
    entities = [
        (0.05, 0.65, 0.22, 0.25, "USERS (users)", "PK id: Integer\nemail: String(Unique)\nhashed_password: String\nrole: Enum(ADMIN, USER, AUDITOR)\nis_active, mfa_enabled\nmfa_secret: String\nfailed_logins, locked_until", "#EEF2FF", "#4338CA"),
        (0.38, 0.65, 0.24, 0.25, "FILES (files)", "PK id: Integer\nFK user_id -> users.id\nFK folder_id -> folders.id\nfilename, file_size, mime_type\nsha256_hash: String\nstorage_path: String\nis_quarantined: Boolean\nencryption_status: String", "#F0FDF4", "#15803D"),
        (0.72, 0.65, 0.23, 0.25, "PERMISSIONS (permissions)", "PK id: Integer\nFK file_id -> files.id\nFK user_id -> users.id\nrole_preset: Enum(VIEWER, etc)\ncan_read, can_download\ncan_write, can_delete\nexpires_at: DateTime", "#FEF3C7", "#B45309"),
        (0.05, 0.25, 0.22, 0.25, "FOLDERS (folders)", "PK id: Integer\nname: String\nFK parent_id -> folders.id\nFK user_id -> users.id\ncreated_at: DateTime", "#F8FAFC", "#475569"),
        (0.38, 0.25, 0.24, 0.25, "AUDIT_LOGS (audit_logs)", "PK id: Integer\nFK actor_id -> users.id\naction: String\nresource_type, resource_id\nip_address: String\nprev_hash: String(SHA-256)\nlog_hash: String(SHA-256)\ntimestamp: DateTime", "#FDF2F8", "#BE185D"),
        (0.72, 0.25, 0.23, 0.25, "SHARE_LINKS (share_links)", "PK id: Integer\nFK file_id -> files.id\ntoken: String(32-byte)\npassword_hash: String\nexpires_at: DateTime\nmax_downloads: Integer\ndownload_count: Integer\nis_active: Boolean", "#F5F3FF", "#6D28D9")
    ]
    
    for x, y, w, h, title, fields, bg, border in entities:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01",
                                      facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.03, title, ha='center', va='center', fontsize=9, fontweight='bold', color=border)
        ax.text(x + 0.015, y + (h - 0.05)/2, fields, ha='left', va='center', fontsize=7.2, color='#1E293B', fontfamily='monospace')
        
    # Relationships
    render_arrow(ax, 0.27, 0.77, 0.38, 0.77, "1 : N (Owns)")
    render_arrow(ax, 0.62, 0.77, 0.72, 0.77, "1 : N (Shares)")
    render_arrow(ax, 0.16, 0.65, 0.16, 0.50, "1 : N (Folders)")
    render_arrow(ax, 0.27, 0.37, 0.38, 0.65, "1 : N (Contains)")
    render_arrow(ax, 0.50, 0.65, 0.50, 0.50, "1 : N (Scans & Access)")
    render_arrow(ax, 0.62, 0.65, 0.72, 0.40, "1 : N (Public Links)")
    
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "ER_Diagram.png"), bbox_inches='tight')
    fig.savefig(os.path.join(OUTPUT_DIR, "ER_Diagram.svg"), bbox_inches='tight')
    plt.close(fig)

# 5.3 DFD Level 0 (Context Diagram)
def generate_dfd_0():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    ax.axis('off')
    ax.set_title("SecureShare — Data Flow Diagram (DFD) Level 0: System Context", 
                 fontsize=14, fontweight='bold', color='#1F4E79', pad=15)
    
    # Process 0.0
    proc = patches.Circle((0.5, 0.5), 0.16, facecolor="#F0F4F8", edgecolor="#1F4E79", linewidth=2.0)
    ax.add_patch(proc)
    ax.text(0.5, 0.53, "0.0\nSecureShare Platform", ha='center', va='center', fontsize=11, fontweight='bold', color='#1F4E79')
    ax.text(0.5, 0.44, "Continuous Security & File System", ha='center', va='center', fontsize=7.5, color='#555555')
    
    # External Entities
    render_box(ax, 0.05, 0.70, 0.18, 0.12, "👤 Authenticated User", "Upload, Download, Share", "#FFFFFF", "#3B82F6")
    render_box(ax, 0.05, 0.20, 0.18, 0.12, "👤 Public Recipient", "Expiring Shared Link Access", "#FFFFFF", "#3B82F6")
    render_box(ax, 0.77, 0.70, 0.18, 0.12, "🛡️ SOC Administrator", "Quarantine, Audit, CI/CD", "#FFFFFF", "#DC2626")
    render_box(ax, 0.77, 0.20, 0.18, 0.12, "📋 Security Auditor", "Audit Trail Verification", "#FFFFFF", "#16A34A")
    
    # Flows
    render_arrow(ax, 0.23, 0.75, 0.40, 0.60, "Files, Auth, Permissions")
    render_arrow(ax, 0.40, 0.57, 0.23, 0.72, "Decrypted File Streams")
    render_arrow(ax, 0.23, 0.27, 0.40, 0.42, "Share Token & Password")
    render_arrow(ax, 0.40, 0.40, 0.23, 0.24, "Shared Download Stream")
    render_arrow(ax, 0.77, 0.75, 0.60, 0.60, "Quarantine Release/Purge")
    render_arrow(ax, 0.60, 0.57, 0.77, 0.72, "Threat Telemetry & Stats")
    render_arrow(ax, 0.77, 0.27, 0.60, 0.42, "Verify Hash Chain Query")
    render_arrow(ax, 0.60, 0.40, 0.77, 0.24, "Cryptographic Proof Logs")
    
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "DFD_Level_0.png"), bbox_inches='tight')
    fig.savefig(os.path.join(OUTPUT_DIR, "DFD_Level_0.svg"), bbox_inches='tight')
    plt.close(fig)

# 5.4 DFD Level 1
def generate_dfd_1():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.axis('off')
    ax.set_title("SecureShare — Data Flow Diagram (DFD) Level 1: Subsystem Decomposition", 
                 fontsize=14, fontweight='bold', color='#1F4E79', pad=15)
                 
    # 5 Subsystems (Processes)
    subsystems = [
        (0.06, 0.60, 0.16, 0.14, "1.0 Auth & MFA\nManager", "Argon2id + TOTP + JWT", "#EEF2FF", "#4338CA"),
        (0.28, 0.60, 0.16, 0.14, "2.0 6-Stage Threat\nScanner Engine", "MIME, ClamAV, Entropy", "#FEF2F2", "#DC2626"),
        (0.52, 0.60, 0.16, 0.14, "3.0 Cryptographic\nEnvelope Engine", "AES-256-GCM + 96-bit IV", "#F0FDF4", "#15803D"),
        (0.76, 0.60, 0.16, 0.14, "4.0 Access Control\n& Share Engine", "BOLA Guard + DAC Presets", "#FEF3C7", "#B45309"),
        (0.40, 0.15, 0.20, 0.14, "5.0 Audit & SOC\nVerifier Engine", "SHA-256 Hash Chain", "#FDF2F8", "#BE185D")
    ]
    
    for x, y, w, h, title, sub, bg, border in subsystems:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01", facecolor=bg, edgecolor=border, lw=1.6)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2 + 0.02, title, ha='center', va='center', fontsize=9, fontweight='bold', color=border)
        ax.text(x + w/2, y + h/2 - 0.035, sub, ha='center', va='center', fontsize=7, color='#4A5568')
        
    # Data Stores (Horizontal bars)
    stores = [
        (0.20, 0.38, 0.18, 0.08, "D1: PostgreSQL DB\n(Users, Perms, Metadata)"),
        (0.62, 0.38, 0.18, 0.08, "D2: Encrypted Storage\n(/uploads - AES-256-GCM)"),
        (0.28, 0.85, 0.18, 0.07, "D3: Quarantine Vault\n(/quarantine - Air-Gapped)")
    ]
    for x, y, w, h, text in stores:
        rect = patches.Rectangle((x, y), w, h, facecolor="#F8FAFC", edgecolor="#475569", lw=1.2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#1E293B')
        
    # Interconnecting Arrows
    render_arrow(ax, 0.22, 0.67, 0.28, 0.67, "Auth Token")
    render_arrow(ax, 0.44, 0.67, 0.52, 0.67, "Clean Payload")
    render_arrow(ax, 0.68, 0.67, 0.76, 0.67, "File Metadata")
    render_arrow(ax, 0.36, 0.74, 0.36, 0.85, "Infected File")
    render_arrow(ax, 0.60, 0.60, 0.68, 0.46, "Encrypted File Blocks")
    render_arrow(ax, 0.14, 0.60, 0.24, 0.46, "User Sessions")
    render_arrow(ax, 0.38, 0.38, 0.45, 0.29, "Audit Events")
    render_arrow(ax, 0.50, 0.29, 0.50, 0.38, "Chain Verifications")
    
    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "DFD_Level_1.png"), bbox_inches='tight')
    fig.savefig(os.path.join(OUTPUT_DIR, "DFD_Level_1.svg"), bbox_inches='tight')
    plt.close(fig)

# 5.5 Trust Boundary Architecture
def generate_trust_boundary():
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    ax.axis('off')
    ax.set_title("SecureShare — Network Segmentation & Trust Boundary Architecture", 
                 fontsize=14, fontweight='bold', color='#1F4E79', pad=15)
                 
    # 4 Trust Zones
    zones = [
        (0.03, 0.08, 0.20, 0.82, "ZONE 0: Untrusted Public", "Client Browser, Attackers, Public Internet", "#FEE2E2", "#EF4444"),
        (0.27, 0.08, 0.21, 0.82, "ZONE 1: DMZ Presentation Tier", "Nginx Reverse Proxy, React Vite Frontend", "#FEF3C7", "#F59E0B"),
        (0.52, 0.08, 0.21, 0.82, "ZONE 2: Secure Application Tier", "FastAPI Core, 6-Stage Scanner, Crypto Engine", "#DBEAFE", "#3B82F6"),
        (0.77, 0.08, 0.20, 0.82, "ZONE 3: Isolated Data Tier", "PostgreSQL, Encrypted Storage, Quarantine Vault", "#DCFCE7", "#10B981")
    ]
    for x, y, w, h, title, sub, bg, border in zones:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01", facecolor=bg, edgecolor=border, lw=2.0, linestyle="--")
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.04, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=border)
        ax.text(x + w/2, y + h - 0.08, sub, ha='center', va='center', fontsize=7, color='#4A5568')
        
    # Trust Boundaries (Vertical Red Cut-lines)
    for bx, label in [(0.25, "Trust Boundary 1\n(Perimeter Firewall / TLS 1.3)"),
                      (0.50, "Trust Boundary 2\n(JWT / RBAC Middleware Gate)"),
                      (0.75, "Trust Boundary 3\n(Storage POSIX & DB Encryption)")]:
        ax.plot([bx, bx], [0.08, 0.88], 'r-.', lw=2.0, alpha=0.7)
        ax.text(bx, 0.04, label, ha='center', va='center', fontsize=7.5, fontweight='bold', color='#B91C1C')
        
    # Internal components inside zones
    # Zone 0
    render_box(ax, 0.05, 0.60, 0.16, 0.12, "User Web Browser", "React Single-Page UI", "#FFFFFF", "#EF4444")
    render_box(ax, 0.05, 0.30, 0.16, 0.12, "Adversary / Scraper", "Brute Force, Malicious Payloads", "#FFFFFF", "#EF4444")
    # Zone 1
    render_box(ax, 0.29, 0.60, 0.17, 0.12, "Nginx Reverse Proxy", "TLS 1.3 Termination, HSTS", "#FFFFFF", "#F59E0B")
    render_box(ax, 0.29, 0.30, 0.17, 0.12, "Sliding Rate Limiter", "IP & User Quota Defense", "#FFFFFF", "#F59E0B")
    # Zone 2
    render_box(ax, 0.54, 0.65, 0.17, 0.12, "FastAPI Backend API", "Argon2id, JWT, BOLA Guards", "#FFFFFF", "#3B82F6")
    render_box(ax, 0.54, 0.45, 0.17, 0.12, "6-Stage Threat Scanner", "ClamAV, Magic Bytes, Entropy", "#FFFFFF", "#3B82F6")
    render_box(ax, 0.54, 0.25, 0.17, 0.12, "AES-256-GCM Engine", "Envelope Crypto & Hash Chain", "#FFFFFF", "#3B82F6")
    # Zone 3
    render_box(ax, 0.79, 0.65, 0.16, 0.12, "PostgreSQL Database", "Encrypted Connection, Argon2", "#FFFFFF", "#10B981")
    render_box(ax, 0.79, 0.45, 0.16, 0.12, "/uploads Volume", "AES-256 Ciphertext Files", "#FFFFFF", "#10B981")
    render_box(ax, 0.79, 0.25, 0.16, 0.12, "/quarantine Volume", "Isolated Air-Gapped Malware", "#FFFFFF", "#10B981")

    # Connective flows
    render_arrow(ax, 0.21, 0.66, 0.29, 0.66, "HTTPS:443")
    render_arrow(ax, 0.46, 0.66, 0.54, 0.66, "Internal REST")
    render_arrow(ax, 0.71, 0.71, 0.79, 0.71, "TCP:5432")
    render_arrow(ax, 0.71, 0.51, 0.79, 0.51, "POSIX I/O")

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "Trust_Boundary_Architecture.png"), bbox_inches='tight')
    fig.savefig(os.path.join(OUTPUT_DIR, "Trust_Boundary_Architecture.svg"), bbox_inches='tight')
    plt.close(fig)

# 5.6 Attack Tree Diagram
def generate_attack_tree():
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    ax.axis('off')
    ax.set_title("SecureShare — Hierarchical Threat Attack Tree & Mitigation Mapping", 
                 fontsize=14, fontweight='bold', color='#1F4E79', pad=15)
                 
    # Root Goal
    render_box(ax, 0.35, 0.85, 0.30, 0.10, "ROOT GOAL: Compromise\nSecureShare Platform", "", "#FEE2E2", "#DC2626", "#991B1B")
    
    # 4 Main Attack Vectors
    branches = [
        (0.04, 0.60, 0.20, 0.11, "1. Exfiltrate Private Files", "BOLA or Key Cracking"),
        (0.28, 0.60, 0.20, 0.11, "2. Take Over User Account", "Brute Force or Token Theft"),
        (0.52, 0.60, 0.20, 0.11, "3. Execute Remote Code", "Malicious Upload / Parser Vuln"),
        (0.76, 0.60, 0.20, 0.11, "4. Conceal Audit Trail", "Tamper Database Logs")
    ]
    for x, y, w, h, t, s in branches:
        render_box(ax, x, y, w, h, t, s, "#FEF3C7", "#D97706", "#92400E")
        render_arrow(ax, 0.50, 0.85, x + w/2, y + h)
        
    # Leaf Attack Tactics and Controls
    leaves = [
        # Branch 1
        (0.04, 0.35, 0.20, 0.16, "Tactic: BOLA ID tampering\n[Mitigation: SC-10 Strict\nownership check & RBAC]\n\nTactic: Crack Ciphertext\n[Mitigation: SC-07 AES-256-GCM\nwith 96-bit unique IV]"),
        # Branch 2
        (0.28, 0.35, 0.20, 0.16, "Tactic: Password Guessing\n[Mitigation: SC-01 Argon2id +\n5-attempt lockout]\n\nTactic: Bypass MFA\n[Mitigation: SC-03 TOTP 30s\nsingle-use code enforcement]"),
        # Branch 3
        (0.52, 0.35, 0.20, 0.16, "Tactic: Upload .php / .exe\n[Mitigation: SC-04 Magic bytes\nwhitelist + ClamAV scan]\n\nTactic: Zip Bomb Overflow\n[Mitigation: SC-04 50MB ceiling\n& compression ratio check]"),
        # Branch 4
        (0.76, 0.35, 0.20, 0.16, "Tactic: Alter DB log rows\n[Mitigation: SC-12 SHA-256\nblockchain hash chaining]\n\nTactic: Delete Audit Tables\n[Mitigation: Read-only Auditor\nrole & automated verifier]")
    ]
    for idx, (x, y, w, h, text) in enumerate(leaves):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01", facecolor="#F0FDF4", edgecolor="#16A34A", lw=1.2)
        ax.add_patch(rect)
        ax.text(x + 0.01, y + h/2, text, ha='left', va='center', fontsize=7.2, color='#1E293B')
        render_arrow(ax, branches[idx][0] + branches[idx][2]/2, 0.60, x + w/2, y + h)

    # Footer
    ax.text(0.5, 0.12, "Summary: Every branch is fully intercepted by Defense-in-Depth controls, eliminating single points of failure.", 
            ha='center', va='center', fontsize=9, fontstyle='italic', color='#1F4E79')

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "Attack_Tree.png"), bbox_inches='tight')
    fig.savefig(os.path.join(OUTPUT_DIR, "Attack_Tree.svg"), bbox_inches='tight')
    plt.close(fig)

# 5.7 Secure Architecture Diagram
def generate_secure_architecture():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=300)
    ax.axis('off')
    ax.set_title("SecureShare — Full End-to-End Secure System Architecture", 
                 fontsize=14, fontweight='bold', color='#1F4E79', pad=15)
                 
    # Frontend Layer
    render_box(ax, 0.05, 0.70, 0.25, 0.16, "Frontend Layer\n(React 18 + Vite + TS)", 
               "• Tailwind CSS Glassmorphism\n• Strict CSP & Input Sanitization\n• AuthContext & Protected Routes\n• In-Memory JWT Access Token", "#EEF2FF", "#4338CA")
               
    # API Gateway / Middleware
    render_box(ax, 0.38, 0.70, 0.25, 0.16, "API Gateway / Security Layer\n(FastAPI Middleware)", 
               "• Sliding-Window Rate Limiter\n• CORS & Anti-Clickjacking\n• JWT Bearer Token Validation\n• RBAC & BOLA Authorization Guard", "#FEF3C7", "#D97706")
               
    # Core Application Engines
    render_box(ax, 0.70, 0.70, 0.25, 0.16, "Application Core Engines\n(FastAPI Services)", 
               "• 6-Stage Malware Scanner Engine\n• AES-256-GCM Envelope Crypto\n• SHA-256 Blockchain Audit Trail\n• Expiring Share Link Engine", "#F0FDF4", "#15803D")
               
    # Storage & Database Tier
    render_box(ax, 0.05, 0.30, 0.25, 0.16, "Database Persistence\n(PostgreSQL / SQLite)", 
               "• Argon2id Hashed Passwords\n• Granular DAC Permissions\n• Audit Ledger with SHA-256 Chain\n• TLS Encrypted Connection Pool", "#F8FAFC", "#475569")
               
    render_box(ax, 0.38, 0.30, 0.25, 0.16, "Encrypted File Vault\n(/storage/uploads)", 
               "• AES-256-GCM Encrypted Payloads\n• Random 96-bit Nonce per File\n• Zero Plaintext Stored on Disk\n• Streaming Decrypt-on-the-Fly", "#ECFDF5", "#059669")
               
    render_box(ax, 0.70, 0.30, 0.25, 0.16, "Quarantine Storage Vault\n(/storage/quarantine)", 
               "• Isolated Air-Gapped Folder\n• Download Air-Gap (403 Forbidden)\n• POSIX Non-Executable Permissions\n• Admin Purge & Review Only", "#FEF2F2", "#DC2626")
               
    # CI/CD DevSecOps Layer
    render_box(ax, 0.15, 0.05, 0.70, 0.12, "DevSecOps Continuous Security CI/CD Pipeline (GitHub Actions)", 
               "• Bandit SAST  |  • Safety & Pip-Audit SCA  |  • TruffleHog Secrets  |  • OWASP ZAP DAST  |  • Security Fuzzing", "#F1F5F9", "#0F172A")
               
    # Connectors
    render_arrow(ax, 0.30, 0.78, 0.38, 0.78, "HTTPS / REST")
    render_arrow(ax, 0.63, 0.78, 0.70, 0.78, "Internal Handlers")
    render_arrow(ax, 0.50, 0.70, 0.18, 0.46, "ORM Queries")
    render_arrow(ax, 0.82, 0.70, 0.50, 0.46, "Encrypted Stream")
    render_arrow(ax, 0.82, 0.70, 0.82, 0.46, "Threat Quarantining")
    render_arrow(ax, 0.50, 0.30, 0.50, 0.17, "Automated Security Tests")

    plt.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "Secure_Architecture.png"), bbox_inches='tight')
    fig.savefig(os.path.join(OUTPUT_DIR, "Secure_Architecture.svg"), bbox_inches='tight')
    plt.close(fig)

# -------------------------------------------------------------
# 6. Generate DRAW.IO Native XML Diagrams
# -------------------------------------------------------------
def make_drawio_xml(name, xml_content):
    filepath = os.path.join(OUTPUT_DIR, f"{name}.drawio")
    full_xml = f"""<mxfile host="app.diagrams.net" modified="2026-10-01T00:00:00.000Z" agent="SecureShare Architect" version="21.0.0" type="device">
  <diagram id="{name}" name="{name}">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1100" pageHeight="850" background="#FFFFFF">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
{xml_content}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(full_xml)

def generate_all_drawio_files():
    # Use Case
    make_drawio_xml("Use_Case_Diagram", """
        <mxCell id="2" value="Regular User" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#E2E8F0;strokeColor=#1F4E79;" vertex="1" parent="1">
          <mxGeometry x="80" y="240" width="40" height="80" as="geometry" />
        </mxCell>
        <mxCell id="3" value="System Admin" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#FEE2E2;strokeColor=#DC2626;" vertex="1" parent="1">
          <mxGeometry x="960" y="240" width="40" height="80" as="geometry" />
        </mxCell>
        <mxCell id="4" value="SecureShare System Boundary" style="shape=rect;html=1;whiteSpace=wrap;fillColor=#F8FAFC;strokeColor=#1F4E79;strokeWidth=2;verticalAlign=top;fontStyle=1;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="220" y="80" width="660" height="660" as="geometry" />
        </mxCell>
        <mxCell id="5" value="UC-01: Argon2id Registration" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1F4E79;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="260" y="140" width="220" height="60" as="geometry" />
        </mxCell>
        <mxCell id="6" value="UC-04: 6-Stage Malware Scanner" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1F4E79;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="580" y="140" width="220" height="60" as="geometry" />
        </mxCell>
        <mxCell id="7" value="UC-05: AES-256-GCM Encryption" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1F4E79;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="260" y="250" width="220" height="60" as="geometry" />
        </mxCell>
        <mxCell id="8" value="UC-10: SHA-256 Audit Verification" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1F4E79;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="580" y="250" width="220" height="60" as="geometry" />
        </mxCell>
        <mxCell id="9" value="UC-11: Admin Quarantine Purge" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1F4E79;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="580" y="370" width="220" height="60" as="geometry" />
        </mxCell>
    """)
    
    # ER
    make_drawio_xml("ER_Diagram", """
        <mxCell id="10" value="USERS&#xa;-------------&#xa;+ id: Integer (PK)&#xa;+ email: String&#xa;+ hashed_password: String&#xa;+ role: String&#xa;+ mfa_secret: String" style="shape=table;whiteSpace=wrap;html=1;fillColor=#EEF2FF;strokeColor=#4338CA;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="120" width="200" height="150" as="geometry" />
        </mxCell>
        <mxCell id="11" value="FILES&#xa;-------------&#xa;+ id: Integer (PK)&#xa;+ user_id: Integer (FK)&#xa;+ filename: String&#xa;+ sha256_hash: String&#xa;+ is_quarantined: Boolean" style="shape=table;whiteSpace=wrap;html=1;fillColor=#F0FDF4;strokeColor=#15803D;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="450" y="120" width="200" height="150" as="geometry" />
        </mxCell>
        <mxCell id="12" value="AUDIT_LOGS&#xa;-------------&#xa;+ id: Integer (PK)&#xa;+ actor_id: Integer (FK)&#xa;+ action: String&#xa;+ prev_hash: String&#xa;+ log_hash: String" style="shape=table;whiteSpace=wrap;html=1;fillColor=#FDF2F8;strokeColor=#BE185D;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="450" y="380" width="200" height="150" as="geometry" />
        </mxCell>
    """)
    
    # DFD Level 0
    make_drawio_xml("DFD_Level_0", """
        <mxCell id="20" value="0.0&#xa;SecureShare&#xa;Platform" style="shape=ellipse;whiteSpace=wrap;html=1;fillColor=#F0F4F8;strokeColor=#1F4E79;strokeWidth=2;fontStyle=1;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="460" y="240" width="180" height="180" as="geometry" />
        </mxCell>
        <mxCell id="21" value="User Browser" style="shape=rect;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#3B82F6;strokeWidth=1.5;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="270" width="150" height="120" as="geometry" />
        </mxCell>
        <mxCell id="22" value="SOC Admin" style="shape=rect;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#DC2626;strokeWidth=1.5;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="850" y="270" width="150" height="120" as="geometry" />
        </mxCell>
    """)

    # DFD Level 1
    make_drawio_xml("DFD_Level_1", """
        <mxCell id="30" value="1.0 Auth &amp; MFA" style="shape=rect;rounded=1;whiteSpace=wrap;html=1;fillColor=#EEF2FF;strokeColor=#4338CA;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="120" y="200" width="160" height="100" as="geometry" />
        </mxCell>
        <mxCell id="31" value="2.0 6-Stage Scanner" style="shape=rect;rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF2F2;strokeColor=#DC2626;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="380" y="200" width="160" height="100" as="geometry" />
        </mxCell>
        <mxCell id="32" value="3.0 AES-256 Crypto" style="shape=rect;rounded=1;whiteSpace=wrap;html=1;fillColor=#F0FDF4;strokeColor=#15803D;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="640" y="200" width="160" height="100" as="geometry" />
        </mxCell>
    """)

    # Trust Boundary
    make_drawio_xml("Trust_Boundary_Architecture", """
        <mxCell id="40" value="ZONE 0: Untrusted Public" style="shape=rect;dashed=1;whiteSpace=wrap;html=1;fillColor=#FEE2E2;strokeColor=#EF4444;strokeWidth=2;verticalAlign=top;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="50" y="100" width="220" height="500" as="geometry" />
        </mxCell>
        <mxCell id="41" value="ZONE 1: DMZ Presentation" style="shape=rect;dashed=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#F59E0B;strokeWidth=2;verticalAlign=top;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="310" y="100" width="220" height="500" as="geometry" />
        </mxCell>
        <mxCell id="42" value="ZONE 2: Secure App Tier" style="shape=rect;dashed=1;whiteSpace=wrap;html=1;fillColor=#DBEAFE;strokeColor=#3B82F6;strokeWidth=2;verticalAlign=top;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="570" y="100" width="220" height="500" as="geometry" />
        </mxCell>
        <mxCell id="43" value="ZONE 3: Isolated Data Tier" style="shape=rect;dashed=1;whiteSpace=wrap;html=1;fillColor=#DCFCE7;strokeColor=#10B981;strokeWidth=2;verticalAlign=top;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="830" y="100" width="220" height="500" as="geometry" />
        </mxCell>
    """)

    # Attack Tree
    make_drawio_xml("Attack_Tree", """
        <mxCell id="50" value="ROOT: Compromise SecureShare" style="shape=rect;rounded=1;whiteSpace=wrap;html=1;fillColor=#FEE2E2;strokeColor=#DC2626;strokeWidth=2;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="400" y="80" width="300" height="70" as="geometry" />
        </mxCell>
        <mxCell id="51" value="1. Exfiltrate Files" style="shape=rect;rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="100" y="220" width="180" height="60" as="geometry" />
        </mxCell>
        <mxCell id="52" value="2. Take Over Accounts" style="shape=rect;rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="340" y="220" width="180" height="60" as="geometry" />
        </mxCell>
        <mxCell id="53" value="3. Execute Code" style="shape=rect;rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="580" y="220" width="180" height="60" as="geometry" />
        </mxCell>
        <mxCell id="54" value="4. Conceal Logs" style="shape=rect;rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="820" y="220" width="180" height="60" as="geometry" />
        </mxCell>
    """)

    # Secure Architecture
    make_drawio_xml("Secure_Architecture", """
        <mxCell id="60" value="Frontend (React 18 + Vite + TS)" style="shape=rect;rounded=1;whiteSpace=wrap;html=1;fillColor=#EEF2FF;strokeColor=#4338CA;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="80" y="160" width="250" height="120" as="geometry" />
        </mxCell>
        <mxCell id="61" value="API Gateway / Middleware" style="shape=rect;rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="420" y="160" width="250" height="120" as="geometry" />
        </mxCell>
        <mxCell id="62" value="Application Core &amp; Crypto" style="shape=rect;rounded=1;whiteSpace=wrap;html=1;fillColor=#F0FDF4;strokeColor=#15803D;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="760" y="160" width="250" height="120" as="geometry" />
        </mxCell>
    """)

def main():
    print("[*] Generating all diagram image files and charts in artifacts/diagrams/ ...")
    generate_risk_heatmap()
    generate_burndown_chart()
    generate_velocity_chart()
    generate_sprint_board()
    generate_use_case_diagram()
    generate_er_diagram()
    generate_dfd_0()
    generate_dfd_1()
    generate_trust_boundary()
    generate_attack_tree()
    generate_secure_architecture()
    generate_all_drawio_files()
    print("[+] Successfully generated all diagram formats (.png, .svg, .drawio)!")

if __name__ == "__main__":
    main()
