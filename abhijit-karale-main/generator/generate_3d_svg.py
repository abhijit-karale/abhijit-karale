"""Script to generate assets/silicon-stack-3d.svg
Creates a stunning 3D isometric visualization of Abhijit Karale's 3 Technical Pillars:
1. Top Slab: Silicon Verification & Signoff (UVM 1.2, JasperGold, SVA)
2. Mid Slab: RTL & Digital Microarchitecture (RV32I Core, AMBA, CDC FIFO)
3. Base Slab: Embedded Firmware & Hardware Bring-Up (STM32, Cortex-M, FreeRTOS)
"""

import math

def generate_silicon_stack_3d_svg(output_path: str):
    width = 960
    height = 540

    # Isometric projection helper
    # In isometric:
    # iso_x = (x - y) * cos(30 deg)
    # iso_y = (x + y) * sin(30 deg) - z
    cos30 = math.cos(math.radians(30))
    sin30 = math.sin(math.radians(30))

    cx = 360 # center X of isometric stack
    cy = 380 # center Y base of isometric stack

    def project(x, y, z):
        # x: right-down, y: left-down, z: straight up
        px = cx + (x - y) * cos30
        py = cy + (x + y) * sin30 - z
        return round(px, 1), round(py, 1)

    # Let slab size be width=240, length=240, slab_thickness=18
    sw = 120
    sl = 120
    thick = 16

    # 3 layers elevations:
    # Layer 1 (Embedded): z=0
    # Layer 2 (RTL): z=120
    # Layer 3 (DV): z=240

    def make_slab(z, col_top, col_left, col_right, stroke_top, label_title, label_sub):
        # 4 corners of top face:
        # P0: (-sw, -sl, z+thick) [top]
        # P1: ( sw, -sl, z+thick) [right]
        # P2: ( sw,  sl, z+thick) [bottom]
        # P3: (-sw,  sl, z+thick) [left]
        t0 = project(-sw, -sl, z + thick)
        t1 = project(sw, -sl, z + thick)
        t2 = project(sw, sl, z + thick)
        t3 = project(-sw, sl, z + thick)

        # 4 corners of bottom face:
        b0 = project(-sw, -sl, z)
        b1 = project(sw, -sl, z)
        b2 = project(sw, sl, z)
        b3 = project(-sw, sl, z)

        # Shadow beneath slab
        s0 = project(-sw - 10, -sl - 10, z - 8)
        s1 = project(sw + 10, -sl - 10, z - 8)
        s2 = project(sw + 10, sl + 10, z - 8)
        s3 = project(-sw - 10, sl + 10, z - 8)

        slab_svg = []
        # Shadow
        slab_svg.append(f'<polygon points="{s0[0]},{s0[1]} {s1[0]},{s1[1]} {s2[0]},{s2[1]} {s3[0]},{s3[1]}" fill="#070305" opacity="0.6" filter="url(#drop_blur)"/>')

        # Left side face (between t3, t2, b2, b3)
        slab_svg.append(f'<polygon points="{t3[0]},{t3[1]} {t2[0]},{t2[1]} {b2[0]},{b2[1]} {b3[0]},{b3[1]}" fill="{col_left}" stroke="#451126" stroke-width="0.8"/>')

        # Right side face (between t1, t2, b2, b1)
        slab_svg.append(f'<polygon points="{t1[0]},{t1[1]} {t2[0]},{t2[1]} {b2[0]},{b2[1]} {b1[0]},{b1[1]}" fill="{col_right}" stroke="#451126" stroke-width="0.8"/>')

        # Top face
        slab_svg.append(f'<polygon points="{t0[0]},{t0[1]} {t1[0]},{t1[1]} {t2[0]},{t2[1]} {t3[0]},{t3[1]}" fill="{col_top}" stroke="{stroke_top}" stroke-width="1.2"/>')

        return "\n".join(slab_svg), t0, t1, t2, t3

    # Generate SVGs
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" xml:space="preserve">')
    svg.append('''<defs>
    <!-- Background Gradient -->
    <linearGradient id="bg_3d" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0E050A"/>
      <stop offset="50%" stop-color="#160810"/>
      <stop offset="100%" stop-color="#0E050A"/>
    </linearGradient>

    <!-- Radial Glows -->
    <radialGradient id="glow_l3" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#E5B5C7" stop-opacity="0.25"/>
      <stop offset="50%" stop-color="#701A3D" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#0E050A" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="glow_cyan" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#64FFDA" stop-opacity="0.2"/>
      <stop offset="60%" stop-color="#0E050A" stop-opacity="0"/>
    </radialGradient>

    <!-- Top Face Gradients -->
    <linearGradient id="top_l1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#240D1A"/>
      <stop offset="100%" stop-color="#160710"/>
    </linearGradient>

    <linearGradient id="top_l2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#3A1124"/>
      <stop offset="100%" stop-color="#1E0A14"/>
    </linearGradient>

    <linearGradient id="top_l3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#551430"/>
      <stop offset="100%" stop-color="#280C1A"/>
    </linearGradient>

    <!-- Filter for Glows -->
    <filter id="neon_glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="drop_blur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>

    <!-- Background Grid -->
    <pattern id="grid_iso" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#701A3D" stroke-width="0.5" stroke-opacity="0.18"/>
    </pattern>
  </defs>

  <style>
    .ak-mono { font-family: 'SF Mono', 'Cascadia Code', 'Fira Code', 'Roboto Mono', Consolas, monospace; }
    .ak-sans { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Roboto, sans-serif; }
    .txt-tag { font-size: 10px; font-weight: 700; letter-spacing: 0.1em; }
    .txt-title { font-size: 15px; font-weight: 800; fill: #FFFFFF; }
    .txt-desc { font-size: 11.5px; font-weight: 400; fill: #E5B5C7; }
    .txt-code { font-size: 11px; font-weight: 600; fill: #F8F0F3; }
    .pulse-bus { stroke-dasharray: 8 6; animation: dash 2.5s linear infinite; }
    @keyframes dash { to { stroke-dashoffset: -28; } }
  </style>

  <!-- Background Base -->
  <rect width="100%" height="100%" fill="url(#bg_3d)"/>
  <rect width="100%" height="100%" fill="url(#grid_iso)"/>

  <!-- Top Ambient Glow -->
  <circle cx="360" cy="180" r="220" fill="url(#glow_l3)"/>
  <circle cx="280" cy="130" r="140" fill="url(#glow_cyan)"/>

  <!-- Header Banner Section in SVG -->
  <g transform="translate(36, 42)">
    <rect x="0" y="0" width="12" height="12" fill="#701A3D" rx="2" stroke="#C77B9B" stroke-width="1"/>
    <rect x="3" y="3" width="6" height="6" fill="#64FFDA" rx="1"/>
    <text x="24" y="10" fill="#64FFDA" class="ak-mono txt-tag">3D SILICON ARCHITECTURE &amp; VERIFICATION STACK</text>
    <text x="0" y="34" class="ak-sans txt-title" font-size="20">Cross-Layer Hardware Intuition: Firmware ➔ RTL ➔ Verification</text>
    <text x="0" y="52" class="ak-sans txt-desc" fill="#C77B9B">Co-designing digital microarchitectures from bare-metal bring-up to silicon-grade UVM formal closure.</text>
  </g>
''')

    # Draw vertical connector columns / bus vias in background
    # 4 corner vias:
    via_offsets = [(-sw + 15, -sl + 15), (sw - 15, -sl + 15), (sw - 15, sl - 15), (-sw + 15, sl - 15)]
    for vx, vy in via_offsets:
        p_base = project(vx, vy, 0)
        p_top = project(vx, vy, 240 + thick)
        svg.append(f'  <line x1="{p_base[0]}" y1="{p_base[1]}" x2="{p_top[0]}" y2="{p_top[1]}" stroke="#701A3D" stroke-width="2" opacity="0.45"/>')
        svg.append(f'  <line x1="{p_base[0]}" y1="{p_base[1]}" x2="{p_top[0]}" y2="{p_top[1]}" stroke="#E5B5C7" stroke-width="1.2" class="pulse-bus" opacity="0.8"/>')

    # Central Vertical Dataflow Bus
    pc_base = project(0, 0, 0)
    pc_top = project(0, 0, 240 + thick)
    svg.append(f'  <!-- Central 3D Optical Bus -->')
    svg.append(f'  <line x1="{pc_base[0]}" y1="{pc_base[1]}" x2="{pc_top[0]}" y2="{pc_top[1]}" stroke="#64FFDA" stroke-width="2.5" filter="url(#neon_glow)" opacity="0.85"/>')
    svg.append(f'  <line x1="{pc_base[0]}" y1="{pc_base[1]}" x2="{pc_top[0]}" y2="{pc_top[1]}" stroke="#FFFFFF" stroke-width="1" class="pulse-bus"/>')

    # LAYER 1: Base - Embedded Firmware & Hardware Bring-Up
    l1_svg, l1_0, l1_1, l1_2, l1_3 = make_slab(
        z=0,
        col_top="url(#top_l1)",
        col_left="#14060E",
        col_right="#0F040A",
        stroke_top="#701A3D",
        label_title="LAYER 01: EMBEDDED PLATFORM",
        label_sub="Bare-metal HAL, FreeRTOS, STM32/ARM Cortex"
    )
    svg.append(f'  <!-- LAYER 1 (BASE) -->\n  <g id="layer1">\n{l1_svg}')

    # Trace geometry on top face of Layer 1 (PCB traces)
    pt1 = project(-60, -60, thick)
    pt2 = project(0, -60, thick)
    pt3 = project(0, 0, thick)
    pt4 = project(60, 0, thick)
    svg.append(f'    <polyline points="{pt1[0]},{pt1[1]} {pt2[0]},{pt2[1]} {pt3[0]},{pt3[1]} {pt4[0]},{pt4[1]}" fill="none" stroke="#C77B9B" stroke-width="1.2" opacity="0.6"/>')
    svg.append(f'    <circle cx="{pt1[0]}" cy="{pt1[1]}" r="2" fill="#E5B5C7"/>')
    svg.append(f'    <circle cx="{pt4[0]}" cy="{pt4[1]}" r="2" fill="#64FFDA"/>')

    # Layer 1 IC Chip in Center
    chip1_0 = project(-30, -30, thick + 4)
    chip1_1 = project(30, -30, thick + 4)
    chip1_2 = project(30, 30, thick + 4)
    chip1_3 = project(-30, 30, thick + 4)
    svg.append(f'    <polygon points="{chip1_0[0]},{chip1_0[1]} {chip1_1[0]},{chip1_1[1]} {chip1_2[0]},{chip1_2[1]} {chip1_3[0]},{chip1_3[1]}" fill="#2B0E1D" stroke="#701A3D" stroke-width="1"/>')
    chip1_c = project(0, 0, thick + 5)
    svg.append(f'    <text x="{chip1_c[0]}" y="{chip1_c[1] + 3}" fill="#E5B5C7" class="ak-mono" font-size="8.5" font-weight="700" text-anchor="middle">STM32 / MCU</text>')
    svg.append('  </g>')

    # LAYER 2: RTL & Digital Microarchitecture
    l2_svg, l2_0, l2_1, l2_2, l2_3 = make_slab(
        z=110,
        col_top="url(#top_l2)",
        col_left="#220A15",
        col_right="#19060F",
        stroke_top="#C77B9B",
        label_title="LAYER 02: RTL MICROARCHITECTURE",
        label_sub="RV32I Core, AMBA Interconnect, CDC FIFO"
    )
    svg.append(f'  <!-- LAYER 2 (MID) -->\n  <g id="layer2">\n{l2_svg}')

    # Trace & pipeline stages on Layer 2
    p_if = project(-55, -20, 110 + thick + 3)
    p_id = project(-25, -20, 110 + thick + 3)
    p_ex = project(5, -20, 110 + thick + 3)
    p_mem = project(35, -20, 110 + thick + 3)
    p_wb = project(65, -20, 110 + thick + 3)
    
    # 5 pipeline blocks
    for px, label in [(p_if, "IF"), (p_id, "ID"), (p_ex, "EX"), (p_mem, "MEM"), (p_wb, "WB")]:
        svg.append(f'    <circle cx="{px[0]}" cy="{px[1]}" r="6" fill="#701A3D" stroke="#E5B5C7" stroke-width="1"/>')
        svg.append(f'    <text x="{px[0]}" y="{px[1] + 2.5}" fill="#F8F0F3" class="ak-mono" font-size="6.5" font-weight="800" text-anchor="middle">{label}</text>')
    svg.append(f'    <line x1="{p_if[0]}" y1="{p_if[1]}" x2="{p_wb[0]}" y2="{p_wb[1]}" stroke="#E5B5C7" stroke-width="1" stroke-dasharray="2 2" opacity="0.7"/>')

    # Interconnect block
    chip2_0 = project(-35, 10, 110 + thick + 3)
    chip2_1 = project(35, 10, 110 + thick + 3)
    chip2_2 = project(35, 45, 110 + thick + 3)
    chip2_3 = project(-35, 45, 110 + thick + 3)
    svg.append(f'    <polygon points="{chip2_0[0]},{chip2_0[1]} {chip2_1[0]},{chip2_1[1]} {chip2_2[0]},{chip2_2[1]} {chip2_3[0]},{chip2_3[1]}" fill="#3D1225" stroke="#C77B9B" stroke-width="1"/>')
    chip2_c = project(0, 28, 110 + thick + 4)
    svg.append(f'    <text x="{chip2_c[0]}" y="{chip2_c[1] + 3}" fill="#FFFFFF" class="ak-mono" font-size="8.5" font-weight="700" text-anchor="middle">AMBA APB / AXI</text>')
    svg.append('  </g>')

    # LAYER 3: Silicon Verification & Signoff
    l3_svg, l3_0, l3_1, l3_2, l3_3 = make_slab(
        z=220,
        col_top="url(#top_l3)",
        col_left="#330D1E",
        col_right="#240714",
        stroke_top="#E5B5C7",
        label_title="LAYER 03: VERIFICATION SIGNOFF",
        label_sub="UVM 1.2 TB, SVA Formal FPV, 95%+ Coverage"
    )
    svg.append(f'  <!-- LAYER 3 (TOP) -->\n  <g id="layer3">\n{l3_svg}')

    # Glowing UVM Architecture loop on top face
    u1 = project(-50, -50, 220 + thick + 2)
    u2 = project(50, -50, 220 + thick + 2)
    u3 = project(50, 50, 220 + thick + 2)
    u4 = project(-50, 50, 220 + thick + 2)
    svg.append(f'    <polygon points="{u1[0]},{u1[1]} {u2[0]},{u2[1]} {u3[0]},{u3[1]} {u4[0]},{u4[1]}" fill="none" stroke="#64FFDA" stroke-width="1.5" stroke-dasharray="6 4" filter="url(#neon_glow)"/>')
    
    # 4 Nodes: Driver, Monitor, Scoreboard, Sequencer
    labels_uvm = [(u1, "SEQ"), (u2, "DRV"), (u3, "MON"), (u4, "SCB")]
    for upos, ulabel in labels_uvm:
        svg.append(f'    <circle cx="{upos[0]}" cy="{upos[1]}" r="7" fill="#14060E" stroke="#64FFDA" stroke-width="1.2"/>')
        svg.append(f'    <text x="{upos[0]}" y="{upos[1] + 3}" fill="#64FFDA" class="ak-mono" font-size="7" font-weight="800" text-anchor="middle">{ulabel}</text>')

    # Center Chip: JasperGold / FPV Engine
    chip3_0 = project(-22, -22, 220 + thick + 4)
    chip3_1 = project(22, -22, 220 + thick + 4)
    chip3_2 = project(22, 22, 220 + thick + 4)
    chip3_3 = project(-22, 22, 220 + thick + 4)
    svg.append(f'    <polygon points="{chip3_0[0]},{chip3_0[1]} {chip3_1[0]},{chip3_1[1]} {chip3_2[0]},{chip3_2[1]} {chip3_3[0]},{chip3_3[1]}" fill="#701A3D" stroke="#64FFDA" stroke-width="1.2"/>')
    chip3_c = project(0, 0, 220 + thick + 5)
    svg.append(f'    <text x="{chip3_c[0]}" y="{chip3_c[1] + 3}" fill="#FFFFFF" class="ak-mono" font-size="8" font-weight="800" text-anchor="middle">SVA PROOF</text>')
    svg.append('  </g>')

    # RIGHT-HAND TELEMETRY CARDS (Pointing to each 3D Layer)
    card_x = 550
    card_w = 370

    # Card 3: Silicon Verification & Signoff (Linked to Layer 3)
    py3 = project(sw, 0, 220 + thick)[1]
    svg.append(f'''
    <!-- CARD 3 (TOP LAYER) -->
    <g transform="translate({card_x}, {py3 - 50})">
      <line x1="-30" y1="50" x2="0" y2="50" stroke="#64FFDA" stroke-width="1.2" stroke-dasharray="3 3"/>
      <circle cx="-30" cy="50" r="3" fill="#64FFDA"/>
      <rect x="0" y="0" width="{card_w}" height="100" rx="8" fill="#180A13" stroke="#64FFDA" stroke-width="1.2" opacity="0.95"/>
      <rect x="12" y="12" width="70" height="18" rx="4" fill="#701A3D"/>
      <text x="47" y="24" fill="#64FFDA" class="ak-mono txt-tag" text-anchor="middle">LAYER 03</text>
      <rect x="90" y="12" width="130" height="18" rx="4" fill="#14060E" stroke="#64FFDA" stroke-width="0.8"/>
      <text x="155" y="24" fill="#FFFFFF" class="ak-mono txt-tag" text-anchor="middle">UVM &amp; FORMAL SIGNOFF</text>
      <rect x="230" y="12" width="76" height="18" rx="4" fill="#0D2E26"/>
      <text x="268" y="24" fill="#64FFDA" class="ak-mono txt-tag" text-anchor="middle">PASS 95%+</text>
      
      <text x="14" y="52" class="ak-sans txt-title" font-size="13">Design Verification &amp; JasperGold FPV</text>
      <text x="14" y="70" class="ak-mono txt-desc" fill="#E5B5C7">• UVM 1.2 Testbenches (Drivers, Monitors, Scoreboards)</text>
      <text x="14" y="86" class="ak-mono txt-desc" fill="#C77B9B">• Cadence Xcelium Functional Coverage | SVA Formal Proofs</text>
    </g>
    ''')

    # Card 2: RTL & Digital Microarchitecture (Linked to Layer 2)
    py2 = project(sw, 0, 110 + thick)[1]
    svg.append(f'''
    <!-- CARD 2 (MID LAYER) -->
    <g transform="translate({card_x}, {py2 - 40})">
      <line x1="-30" y1="42" x2="0" y2="42" stroke="#E5B5C7" stroke-width="1.2" stroke-dasharray="3 3"/>
      <circle cx="-30" cy="42" r="3" fill="#E5B5C7"/>
      <rect x="0" y="0" width="{card_w}" height="95" rx="8" fill="#180A13" stroke="#701A3D" stroke-width="1.2" opacity="0.95"/>
      <rect x="12" y="12" width="70" height="18" rx="4" fill="#701A3D"/>
      <text x="47" y="24" fill="#E5B5C7" class="ak-mono txt-tag" text-anchor="middle">LAYER 02</text>
      <rect x="90" y="12" width="145" height="18" rx="4" fill="#14060E" stroke="#701A3D" stroke-width="0.8"/>
      <text x="162" y="24" fill="#FFFFFF" class="ak-mono txt-tag" text-anchor="middle">RTL MICROARCHITECTURE</text>
      <rect x="245" y="12" width="80" height="18" rx="4" fill="#3D1225"/>
      <text x="285" y="24" fill="#E5B5C7" class="ak-mono txt-tag" text-anchor="middle">RV32I CORE</text>
      
      <text x="14" y="50" class="ak-sans txt-title" font-size="13">Digital Design &amp; Bus Protocols</text>
      <text x="14" y="68" class="ak-mono txt-desc" fill="#E5B5C7">• 5-Stage RV32I Pipelined Core with Forwarding &amp; Hazard Unit</text>
      <text x="14" y="84" class="ak-mono txt-desc" fill="#C77B9B">• AMBA-APB &amp; AXI4-Lite Slaves | Parameterizable CDC FIFOs</text>
    </g>
    ''')

    # Card 1: Embedded Firmware & Hardware Bring-Up (Linked to Layer 1)
    py1 = project(sw, 0, thick)[1]
    svg.append(f'''
    <!-- CARD 1 (BASE LAYER) -->
    <g transform="translate({card_x}, {py1 - 40})">
      <line x1="-30" y1="42" x2="0" y2="42" stroke="#C77B9B" stroke-width="1.2" stroke-dasharray="3 3"/>
      <circle cx="-30" cy="42" r="3" fill="#C77B9B"/>
      <rect x="0" y="0" width="{card_w}" height="95" rx="8" fill="#180A13" stroke="#451126" stroke-width="1.2" opacity="0.95"/>
      <rect x="12" y="12" width="70" height="18" rx="4" fill="#451126"/>
      <text x="47" y="24" fill="#C77B9B" class="ak-mono txt-tag" text-anchor="middle">LAYER 01</text>
      <rect x="90" y="12" width="135" height="18" rx="4" fill="#14060E" stroke="#451126" stroke-width="0.8"/>
      <text x="157" y="24" fill="#FFFFFF" class="ak-mono txt-tag" text-anchor="middle">EMBEDDED PLATFORM</text>
      <rect x="235" y="12" width="85" height="18" rx="4" fill="#3D1225"/>
      <text x="277" y="24" fill="#F59E0B" class="ak-mono txt-tag" text-anchor="middle">2+ YRS PROD</text>
      
      <text x="14" y="50" class="ak-sans txt-title" font-size="13">Firmware, Peripherals &amp; Multi-Layer Bring-Up</text>
      <text x="14" y="68" class="ak-mono txt-desc" fill="#E5B5C7">• STM32, ARM Cortex-M, FreeRTOS Preemptive Multitasking</text>
      <text x="14" y="84" class="ak-mono txt-desc" fill="#C77B9B">• UART/SPI/I2C Drivers • Multi-Layer PCB &amp; DSO/LA Diagnostics</text>
    </g>
    ''')

    # Bottom status telemetry bar
    svg.append('''
  <g transform="translate(36, 500)">
    <rect x="0" y="0" width="888" height="26" rx="5" fill="#14060E" stroke="#451126" stroke-width="1"/>
    <circle cx="16" cy="13" r="4" fill="#64FFDA" filter="url(#neon_glow)"/>
    <text x="28" y="17" fill="#64FFDA" class="ak-mono" font-size="9.5" font-weight="700">STATUS: VERIFICATION CLOSURE READY</text>
    <text x="320" y="17" fill="#E5B5C7" class="ak-mono" font-size="9.5">CADENCE XCELIUM • JASPERGOLD FPV • SYSTEMVERILOG UVM 1.2 • SKY130 FLOW</text>
    <text x="850" y="17" fill="#C77B9B" class="ak-mono" font-size="9.5" text-anchor="end">DIE_TOPOLOGY: 3D_STACK</text>
  </g>
</svg>''')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated 3D SVG at: {output_path}")

if __name__ == "__main__":
    generate_silicon_stack_3d_svg("assets/silicon-stack-3d.svg")
