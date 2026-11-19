"""
KaushalSetu - Recognition of Prior Learning (RPL) Knowledge Base
Contains authentic Qualification Packs (QP) and National Occupational Standards (NOS)
aligned with National Skill Development Corporation (NSDC) and NSQF (National Skills Qualifications Framework).
"""

QUALIFICATION_PACKS = {
    "electrician": {
        "code": "ELE/Q6001",
        "name": "Domestic Electrician",
        "trade_display": "Domestic Electrician",
        "sector": "Electronics & Power",
        "nsqf_level": 4,
        "description": "Performs installation, testing, and maintenance of electrical wiring, equipment, and fixtures in domestic premises according to electrical safety codes.",
        "common_tools": ["Digital Multimeter", "Conduit Bender", "Insulated Screwdrivers", "Wire Stripper", "Megger / Insulation Tester", "Pliers", "Hammer Drill", "Tester Pen"],
        "nos_list": [
            {
                "code": "ELE/N6001",
                "title": "Plan and prepare for installation of electrical components and wiring",
                "weight": 20,
                "keywords": ["plan", "blueprint", "diagram", "layout", "single line", "load calculation", "wire gauge", "copper", "aluminum", "conduit", "pvc", "casing", "capping", "measurement", "survey", "tools"],
                "performance_criteria": [
                    "PC1: Accurately interpret house electrical layout drawings and circuit diagrams.",
                    "PC2: Calculate electrical load requirements for domestic lighting, heating, and power appliances.",
                    "PC3: Select appropriate wire gauge (1.0 sq mm to 6.0 sq mm) based on current carrying capacity.",
                    "PC4: Prepare bill of materials including conduits, junction boxes, wires, switches, and MCBs."
                ],
                "viva_questions": [
                    "How do you determine the required wire size for a 1.5 ton split AC?",
                    "What safety precautions do you take before inspecting an old household wiring system?"
                ]
            },
            {
                "code": "ELE/N6002",
                "title": "Install concealed and surface wiring, conduits, cables, and distribution boards",
                "weight": 25,
                "keywords": ["conduit", "wall chasing", "concealed", "surface", "junction box", "pull wire", "distribution board", "mcb", "elcb", "rccb", "neutral", "phase", "earthing", "switchboard", "busbar"],
                "performance_criteria": [
                    "PC1: Carry out wall chasing and secure PVC conduits using saddle clamps at regular intervals.",
                    "PC2: Pull phase, neutral, and earth wires through conduits using fish tape without damaging insulation.",
                    "PC3: Assemble and wire distribution boards with appropriate MCB ratings (6A, 16A, 25A, 32A).",
                    "PC4: Install Earth Leakage Circuit Breaker (ELCB) / Residual Current Circuit Breaker (RCCB) for shock prevention."
                ],
                "viva_questions": [
                    "What is the difference between an MCB and an RCCB/ELCB?",
                    "At what height from the floor should switchboards typically be mounted?"
                ]
            },
            {
                "code": "ELE/N6003",
                "title": "Install switches, sockets, luminaires, ceiling fans, and household appliances",
                "weight": 20,
                "keywords": ["switch", "socket", "light fixture", "ceiling fan", "regulator", "geyser", "inverter", "stabilizer", "led", "chandelier", "two-way switch", "staircase wiring", "exhaust fan"],
                "performance_criteria": [
                    "PC1: Wire and mount modular switch plates with proper polarity (switch connected to phase wire).",
                    "PC2: Assemble and hang ceiling fans with downrod, safety pin, and connect electronic speed regulator.",
                    "PC3: Wire two-way switches for staircase and corridor illumination.",
                    "PC4: Connect heavy appliances (geysers, room heaters) with dedicated 16A power points and earthing."
                ],
                "viva_questions": [
                    "Why must switches always break the phase wire rather than the neutral wire?",
                    "How do you connect a two-way switch for staircase lighting?"
                ]
            },
            {
                "code": "ELE/N6004",
                "title": "Inspect, test, fault-diagnose, and repair electrical installations",
                "weight": 20,
                "keywords": ["multimeter", "continuity", "megger", "insulation resistance", "voltage", "current", "short circuit", "open circuit", "earth fault", "tripping", "troubleshooting", "repair", "fuse"],
                "performance_criteria": [
                    "PC1: Conduct continuity tests using multimeter to verify circuit integrity without power.",
                    "PC2: Perform insulation resistance test using Megger between conductors and earth (> 1 Megaohm).",
                    "PC3: Diagnose reasons for frequent MCB tripping (overload, short circuit, or insulation breakdown).",
                    "PC4: Replace damaged wiring, faulty switches, loose terminals, or burnt contactors safely."
                ],
                "viva_questions": [
                    "How do you test if a wall socket has proper earthing using a multimeter?",
                    "What reading do you expect on a Megger for a safe domestic installation?"
                ]
            },
            {
                "code": "ELE/N9901",
                "title": "Follow occupational health, safety, earthing, and environmental standards",
                "weight": 15,
                "keywords": ["safety", "ppe", "insulated boots", "gloves", "lockout", "tagout", "earthing", "chemical earthing", "pipe earthing", "earth electrode", "fire extinguisher", "first aid", "shock rescue"],
                "performance_criteria": [
                    "PC1: Use appropriate personal protective equipment (PPE): rubber gloves, insulated boots, and goggles.",
                    "PC2: Verify that power supply is isolated and de-energized before handling live wiring.",
                    "PC3: Construct standard chemical/pipe earthing pit with salt, charcoal, and copper/GI electrode (< 5 ohms).",
                    "PC4: Apply emergency first-aid protocols and CPR in the event of an electric shock victim."
                ],
                "viva_questions": [
                    "What is the permissible resistance value for domestic earthing?",
                    "What immediate action should you take if a coworker suffers an electric shock?"
                ]
            }
        ]
    },

    "plumber": {
        "code": "PSC/Q0104",
        "name": "General Plumber",
        "trade_display": "General Plumber",
        "sector": "Plumbing",
        "nsqf_level": 4,
        "description": "Installs, tests, maintains, and repairs water supply, drainage, sanitary fixtures, and piping networks in residential and commercial premises.",
        "common_tools": ["Pipe Wrench", "Hacksaw", "Pipe Cutter", "CPVC Solvent Cement", "Thread Seal Tape (Teflon)", "Spirit Level", "Pressure Testing Pump", "Drain Auger"],
        "nos_list": [
            {
                "code": "PSC/N0108",
                "title": "Pre-installation checks and layout planning for plumbing systems",
                "weight": 20,
                "keywords": ["plumbing plan", "drawing", "slope", "gradient", "water supply", "overhead tank", "inlet", "outlet", "pipe sizing", "pressure", "gravity flow", "site survey"],
                "performance_criteria": [
                    "PC1: Read and interpret architectural plumbing drawings and drainage route maps.",
                    "PC2: Plan pipe routes maintaining required gradient (1:40 or 1:50) for sewage drainage.",
                    "PC3: Determine water head and select appropriate pipe diameters for supply lines.",
                    "PC4: Calculate material requirements: pipes, bends, tees, reducers, valves, and solvent cement."
                ],
                "viva_questions": [
                    "Why is maintaining the correct pipe slope critical for waste water drainage?",
                    "What is the difference between CPVC and UPVC pipes in domestic plumbing?"
                ]
            },
            {
                "code": "PSC/N0109",
                "title": "Cut, thread, joint, and install water supply and drainage pipelines",
                "weight": 25,
                "keywords": ["cpvc", "upvc", "gi pipe", "threading", "solvent cement", "primer", "teflon tape", "coupler", "elbow", "tee", "union", "clamp", "concealed piping", "leak testing"],
                "performance_criteria": [
                    "PC1: Cut pipes square using pipe cutter or hacksaw and deburr internal/external edges.",
                    "PC2: Apply solvent cement uniformly to CPVC/UPVC joints and hold with correct socket depth.",
                    "PC3: Cut clean threads on GI pipes and apply Teflon tape and hemp before tightening with pipe wrench.",
                    "PC4: Secure pipelines to walls using galvanized clamps at recommended intervals."
                ],
                "viva_questions": [
                    "How long should you wait after making a solvent cement joint before water pressure testing?",
                    "How do you prevent thread leaks on high-pressure GI connections?"
                ]
            },
            {
                "code": "PSC/N0110",
                "title": "Install sanitary fixtures, faucets, showers, geysers, and pumps",
                "weight": 20,
                "keywords": ["wash basin", "water closet", "commode", "flush tank", "shower", "mixer", "bib cock", "angle valve", "geyser", "submersible pump", "pressure pump", "float valve", "trap"],
                "performance_criteria": [
                    "PC1: Align and mount European/Indian water closets ensuring water-tight seal with floor drain.",
                    "PC2: Install wall-hung wash basins with bottle traps and waste couplings without leakage.",
                    "PC3: Mount and connect wall mixers, concealed diverters, and overhead shower heads.",
                    "PC4: Connect water heaters (geysers) with non-return pressure relief safety valves."
                ],
                "viva_questions": [
                    "What is the purpose of a P-trap / S-trap in sanitary plumbing?",
                    "Why must a pressure relief valve never be omitted from a geyser installation?"
                ]
            },
            {
                "code": "PSC/N0111",
                "title": "Diagnose leaks, blockages, pressure drops, and perform repair",
                "weight": 20,
                "keywords": ["leakage", "pressure drop", "air lock", "blockage", "clogged drain", "drain snake", "flange repair", "washer replacement", "valve repair", "cartridge", "seepage"],
                "performance_criteria": [
                    "PC1: Trace hidden water seepage and pipe leaks using pressure test pumps.",
                    "PC2: Clear air locks from overhead supply lines to restore uniform water flow.",
                    "PC3: Dislodge stubborn clogs in traps and sewer pipes using drain snakes/augers.",
                    "PC4: Service dripping faucets by replacing ceramic disc cartridges or rubber washers."
                ],
                "viva_questions": [
                    "How do you bleed an air lock in a gravity-fed water line?",
                    "What steps do you follow to identify hidden wall dampness caused by plumbing leaks?"
                ]
            },
            {
                "code": "PSC/N0136",
                "title": "Comply with workplace safety, hygiene, and environmental sanitation",
                "weight": 15,
                "keywords": ["hygiene", "sanitation", "gloves", "goggles", "boots", "toxic gases", "manhole safety", "water conservation", "waste disposal", "first aid"],
                "performance_criteria": [
                    "PC1: Wear protective equipment when handling drainage lines and hazardous sewer waste.",
                    "PC2: Ensure proper ventilation and gas testing before opening deep septic tanks or manholes.",
                    "PC3: Follow safe disposal of hazardous chemical solvents, adhesives, and old lead pipes.",
                    "PC4: Promote water-saving aerators and dual-flush mechanisms in plumbing installations."
                ],
                "viva_questions": [
                    "What poisonous gases are commonly encountered inside septic tanks, and how do you protect yourself?",
                    "What immediate steps should be taken if solvent cement splashes into an eye?"
                ]
            }
        ]
    },

    "mason": {
        "code": "CON/Q0102",
        "name": "General Mason",
        "trade_display": "General Mason / Bricklayer",
        "sector": "Construction",
        "nsqf_level": 4,
        "description": "Carries out brickwork, blockwork, plastering, pointing, screeding, and structural masonry work in building construction adhering to architectural standards.",
        "common_tools": ["Trowel", "Plumb Bob", "Spirit Level", "Mason's Line / Thread", "Chisel & Club Hammer", "Measuring Tape", "Floats (Wooden & Sponge)", "Mortar Pan / Tassla"],
        "nos_list": [
            {
                "code": "CON/N0105",
                "title": "Prepare mortar mixtures, cement-sand ratios, and staging of materials",
                "weight": 20,
                "keywords": ["mortar", "cement", "sand", "ratio", "water cement ratio", "mixing", "hydration", "lime", "slump", "staging", "brick soaking", "curing"],
                "performance_criteria": [
                    "PC1: Proportion cement and sand accurately (1:4, 1:6) according to specified masonry application.",
                    "PC2: Mix mortar uniformly with controlled water content to achieve proper workability.",
                    "PC3: Pre-soak clay bricks thoroughly in clean water to prevent premature absorption of mortar moisture.",
                    "PC4: Organize mortar trays, bricks, and scaffolding within safe ergonomic reach."
                ],
                "viva_questions": [
                    "Why must clay bricks be submerged in water prior to masonry laying?",
                    "What is the recommended cement-to-sand ratio for interior wall plastering?"
                ]
            },
            {
                "code": "CON/N0106",
                "title": "Construct brickwork, blockwork, and stone masonry using standard bonds",
                "weight": 25,
                "keywords": ["english bond", "flemish bond", "stretcher bond", "header", "frog", "perpend", "bed joint", "thickness", "overlap", "toothing", "block masonry", "aac blocks"],
                "performance_criteria": [
                    "PC1: Lay bricks with frogs facing upward and fill all bed and perpend joints fully with mortar.",
                    "PC2: Maintain consistent 10mm to 12mm mortar joint thickness throughout all courses.",
                    "PC3: Construct English bond and Flemish bond walls with half-bat or queen closer arrangements.",
                    "PC4: Lay Autoclaved Aerated Concrete (AAC) blocks using thin-bed adhesive compounds."
                ],
                "viva_questions": [
                    "What is the key structural difference between English Bond and Flemish Bond?",
                    "Why is the 'frog' of a brick placed facing upwards?"
                ]
            },
            {
                "code": "CON/N0107",
                "title": "Execute wall and ceiling plastering, pointing, screeding, and curing",
                "weight": 20,
                "keywords": ["plaster", "screed", "rendering", "floating", "troweling", "sponge finish", "curing", "groove", "bullmark", "chicken mesh", "column joint", "dampness"],
                "performance_criteria": [
                    "PC1: Establish reference 'bull marks' on walls to ensure uniform 12mm to 15mm plaster thickness.",
                    "PC2: Fix GI chicken wire mesh across RCC beam-masonry junctions to prevent shrinkage cracks.",
                    "PC3: Apply scratch coat and finish coat using wooden floats and metal trowels for smooth plumb finish.",
                    "PC4: Ensure wet curing of plastered surfaces twice daily for a minimum of 7 to 10 days."
                ],
                "viva_questions": [
                    "How do bull marks ensure flat, vertical plastered walls?",
                    "Why is wet curing mandatory for cement masonry and for how many days?"
                ]
            },
            {
                "code": "CON/N0108",
                "title": "Verify alignment, verticality, horizontal level, and corner perpendicularity",
                "weight": 20,
                "keywords": ["plumb bob", "spirit level", "line thread", "right angle", "3-4-5 rule", "corner", "diagonal", "survey", "square", "level tube", "water level"],
                "performance_criteria": [
                    "PC1: Check wall verticality continually using plumb bob at corners, jambs, and wall faces.",
                    "PC2: Check horizontal leveling of courses using water level tube and spirit levels.",
                    "PC3: Check 90-degree square corners using the 3-4-5 geometric rule or steel square.",
                    "PC4: Maintain taut alignment thread along each course from end pillars to prevent bowing."
                ],
                "viva_questions": [
                    "How do you check if a 10-meter foundation corner is exactly 90 degrees using a tape?",
                    "How does a clear plastic water tube establish identical heights across two separate rooms?"
                ]
            },
            {
                "code": "CON/N9001",
                "title": "Comply with construction safety, scaffolding stability, and PPE standards",
                "weight": 15,
                "keywords": ["scaffold", "fall protection", "hard hat", "helmet", "safety harness", "steel toe boots", "eye goggles", "debris disposal", "load bearing", "housekeeping"],
                "performance_criteria": [
                    "PC1: Inspect bamboo/steel scaffolding, toe boards, and anchor points before ascending.",
                    "PC2: Wear helmet, safety harness with lifeline when working at elevations above 2 meters.",
                    "PC3: Clear loose debris, wet mortar spills, and masonry offcuts from work platforms.",
                    "PC4: Follow safe manual handling techniques when lifting heavy cement bags and stone blocks."
                ],
                "viva_questions": [
                    "What safety checklist must be verified before stepping onto elevated scaffolding?",
                    "What is the safe weight-lifting posture to prevent lumbar spinal injury?"
                ]
            }
        ]
    },

    "automotive": {
        "code": "ASC/Q1411",
        "name": "Two-Wheeler Service Technician",
        "trade_display": "Two-Wheeler Service Technician",
        "sector": "Automotive",
        "nsqf_level": 4,
        "description": "Performs diagnostic, repair, servicing, and overhauling work on motorcycles and scooters including engine, transmission, brakes, and electrical subsystems.",
        "common_tools": ["Torque Wrench", "Feeler Gauge", "Compression Tester", "OBD Scanner", "Digital Multimeter", "Chain Breaker & Riveter", "Micrometer", "Spark Plug Gauge"],
        "nos_list": [
            {
                "code": "ASC/N1417",
                "title": "Carry out routine servicing, oil changes, filtration, and tune-up",
                "weight": 20,
                "keywords": ["service", "engine oil", "viscosity", "oil filter", "air filter", "spark plug", "gap", "tappet clearance", "valve clearance", "feeler gauge", "chain lube", "slackness", "carburetor clean"],
                "performance_criteria": [
                    "PC1: Drain engine oil, inspect magnetic drain plug for metal filings, and refill with recommended grade.",
                    "PC2: Clean or replace foam/paper air filters and set spark plug electrode gap with feeler gauge (0.7-0.8mm).",
                    "PC3: Inspect and adjust valve rocker clearance (tappet) using feeler gauges to engine specs.",
                    "PC4: Adjust drive chain tension/slack (20-30mm) and lubricate with high-grade chain lubricant."
                ],
                "viva_questions": [
                    "What does the viscosity grade 20W-40 signify for motorcycle engine oil?",
                    "What symptoms occur if valve tappet clearance is set too tight?"
                ]
            },
            {
                "code": "ASC/N1418",
                "title": "Overhaul and tune fuel systems, clutch, and engine top-end",
                "weight": 25,
                "keywords": ["clutch", "friction plates", "carburetor", "fuel injector", "throttle body", "compression test", "piston rings", "cylinder head", "decarbonizing", "idle speed", "obd", "fuel pump"],
                "performance_criteria": [
                    "PC1: Dismantle and clean carburetor jets, float bowl, and set air-fuel mixture screw.",
                    "PC2: Inspect clutch friction plates, steel plates, and clutch basket fingers for scoring or wear.",
                    "PC3: Measure cylinder bore and piston ring end-gap using feeler gauge inside cylinder sleeve.",
                    "PC4: Connect OBD diagnostic scanner to check fault codes on modern fuel-injected (FI) two-wheelers."
                ],
                "viva_questions": [
                    "How do you diagnose clutch slippage versus clutch dragging?",
                    "What engine symptoms indicate leaking or burnt exhaust valves?"
                ]
            },
            {
                "code": "ASC/N1419",
                "title": "Diagnose, service, and bleed braking systems and suspension",
                "weight": 20,
                "keywords": ["brake", "disc brake", "drum brake", "brake shoes", "brake pads", "caliper", "master cylinder", "brake fluid", "dot4", "bleeding", "telescopic fork", "fork oil", "oil seal", "mono shock"],
                "performance_criteria": [
                    "PC1: Inspect disc brake pad thickness and rotor runout using dial indicator gauge.",
                    "PC2: Flush and bleed hydraulic brake lines to eliminate spongy pedal/lever feel using DOT 3/4 fluid.",
                    "PC3: Inspect drum brake shoe lining thickness and check brake drum internal scoring.",
                    "PC4: Disassemble front telescopic forks, replace leaking fork oil seals, and refill exact fork oil volume."
                ],
                "viva_questions": [
                    "Why must hydraulic brake fluid be changed periodically?",
                    "How do you properly bleed air bubbles from a motorcycle front disc brake line?"
                ]
            },
            {
                "code": "ASC/N1420",
                "title": "Test, diagnose, and repair electrical, ignition, and battery circuits",
                "weight": 20,
                "keywords": ["battery", "multimeter", "charging", "magneto", "stator", "rectifier", "regulator", "starter motor", "relay", "ignition coil", "cdi", "ecu", "wiring harness", "fuse", "headlight"],
                "performance_criteria": [
                    "PC1: Test battery open-circuit voltage (>12.6V) and load test cranking voltage (>9.6V).",
                    "PC2: Measure alternator/stator AC output and Rectifier-Regulator (RR) charging voltage (14.0V-14.5V).",
                    "PC3: Trace electrical parasitic battery drain and short circuits using digital multimeter in series.",
                    "PC4: Test starter motor relay, armature brushes, and bendix drive gear engagement."
                ],
                "viva_questions": [
                    "What is normal battery charging voltage when engine is revved to 3000 RPM?",
                    "How do you test if a starter motor issue is due to the relay or the starter motor brushes?"
                ]
            },
            {
                "code": "ASC/N0001",
                "title": "Maintain garage safety, hazardous fluid handling, and customer handover",
                "weight": 15,
                "keywords": ["workshop safety", "used oil disposal", "battery acid", "fire safety", "exhaust ventilation", "test ride safety", "job card", "customer handover"],
                "performance_criteria": [
                    "PC1: Collect waste engine oil and coolant into sealed drums for certified environmental recycling.",
                    "PC2: Provide adequate exhaust extraction when running internal combustion engines inside the shop.",
                    "PC3: Handle lead-acid battery electrolyte safely with rubber aprons, eye shields, and neutralizing agent.",
                    "PC4: Conduct post-service road test with helmet to confirm brake, steering, and engine readiness."
                ],
                "viva_questions": [
                    "What are the safety hazards of draining hot radiator coolant or engine oil?",
                    "What pre-delivery checklist must be verified before handing a bike to the customer?"
                ]
            }
        ]
    },

    "welder": {
        "code": "CSC/Q0204",
        "name": "Manual Metal Arc Welder",
        "trade_display": "Manual Metal Arc Welder (SMAW / MMAW)",
        "sector": "Capital Goods",
        "nsqf_level": 3,
        "description": "Performs manual metal arc welding (shielded metal arc welding) on carbon steels and alloy plates in various positions following welding procedure specifications (WPS).",
        "common_tools": ["Welding Machine (Inverter/Transformer)", "Electrode Holder & Earth Clamp", "Chipping Hammer & Wire Brush", "Welding Helmet / Face Shield", "Angle Grinder", "Fillet Weld Gauge", "Leather Gloves & Apron"],
        "nos_list": [
            {
                "code": "CSC/N0204",
                "title": "Prepare metal joint edges, beveling, tack welding, and joint fit-up",
                "weight": 25,
                "keywords": ["bevel", "groove", "v-groove", "root face", "root gap", "tack weld", "fit up", "angle grinder", "wire brush", "rust removal", "wps", "mild steel", "carbon steel"],
                "performance_criteria": [
                    "PC1: Clean joint edges of rust, mill scale, paint, oil, and moisture using wire brush or angle grinder.",
                    "PC2: Prepare single V-groove (60-70 degree included angle) with 1.5mm to 2mm root face.",
                    "PC3: Align and maintain uniform root gap (2mm to 3mm) using spacing wire/spacers.",
                    "PC4: Deposit sound tack welds at both ends of the joint without porosity or cracking."
                ],
                "viva_questions": [
                    "Why is maintaining a uniform root gap critical for full penetration welds?",
                    "What defect occurs if weld edges have residual oil, moisture, or rust?"
                ]
            },
            {
                "code": "CSC/N0205",
                "title": "Select electrodes, adjust current, strike arc, and deposit weld passes",
                "weight": 30,
                "keywords": ["electrode", "e6013", "e7018", "current", "amperage", "polarity", "dcep", "dcen", "arc length", "travel speed", "weave", "stringer bead", "slag", "interpass temperature"],
                "performance_criteria": [
                    "PC1: Select correct welding electrode (E6013 for general fabrication, E7018 for structural loads).",
                    "PC2: Set appropriate welding amperage matching electrode diameter (e.g. 90-120A for 3.15mm E6013).",
                    "PC3: Strike and maintain stable electric arc with correct arc length (equal to electrode core diameter).",
                    "PC4: Control travel speed and electrode angle (15-20 degrees drag angle) to produce uniform ripples."
                ],
                "viva_questions": [
                    "What is the difference between E6013 and low-hydrogen E7018 electrodes?",
                    "What happens to the weld bead if your welding current is set too high?"
                ]
            },
            {
                "code": "CSC/N0206",
                "title": "Inspect welds for surface defects, chip slag, grind, and measure profiles",
                "weight": 25,
                "keywords": ["inspection", "visual inspection", "chipping hammer", "slag removal", "wire brush", "undercut", "porosity", "slag inclusion", "spatter", "incomplete penetration", "fillet gauge"],
                "performance_criteria": [
                    "PC1: Chip slag thoroughly after each weld pass and clean with wire brush before subsequent pass.",
                    "PC2: Visually inspect weld bead for undercut, excessive spatter, cracks, and surface porosity.",
                    "PC3: Measure weld leg length and throat thickness using standard fillet weld gauge.",
                    "PC4: Grind out stop-start defects and surface irregularities using angle grinder."
                ],
                "viva_questions": [
                    "What causes 'undercut' defect along the toe of a weld bead?",
                    "How do you verify the throat thickness of a fillet weld?"
                ]
            },
            {
                "code": "CSC/N0207",
                "title": "Adhere to occupational health, arc-flash eye safety, and fire prevention",
                "weight": 20,
                "keywords": ["eye safety", "welding helmet", "shade 10", "shade 11", "arc flash", "uv radiation", "leather apron", "leather gloves", "fire blanket", "fire extinguisher", "fume extraction"],
                "performance_criteria": [
                    "PC1: Wear welding helmet with appropriate filter shade (DIN 10-12) to protect against UV/IR radiation.",
                    "PC2: Wear chrome leather gauntlet gloves, leather apron, and spats to protect against sparks and hot metal.",
                    "PC3: Clear flammable solvents, cotton waste, and gas cylinders from welding vicinity (minimum 10 meters).",
                    "PC4: Ensure adequate ventilation or localized fume extractors when welding in confined spaces."
                ],
                "viva_questions": [
                    "What is 'arc eye' / flash burn, and how is it completely prevented?",
                    "What fire safety equipment must be positioned within immediate arm's reach during welding?"
                ]
            }
        ]
    },

    "tailor": {
        "code": "AMH/Q1947",
        "name": "Self Employed Tailor",
        "trade_display": "Self Employed Tailor",
        "sector": "Apparel, Made-ups & Home Furnishing",
        "nsqf_level": 4,
        "description": "Creates customized garments, takes body measurements, drafts patterns, cuts fabrics, operates sewing machines, and performs garment finishing and alterations.",
        "common_tools": ["Measuring Tape", "Tailor's Chalk", "Dressmaker Shears / Scissors", "Pattern Paper", "Single Needle Lockstitch Machine", "Iron & Pressing Board", "Seam Ripper"],
        "nos_list": [
            {
                "code": "AMH/N1947",
                "title": "Record client body measurements and draft garment patterns",
                "weight": 25,
                "keywords": ["measurement", "tape", "bust", "waist", "hip", "inseam", "shoulder", "armhole", "pattern drafting", "paper pattern", "ease allowance", "design styling", "neckline"],
                "performance_criteria": [
                    "PC1: Take accurate body measurements using flexible measuring tape following anatomical landmarks.",
                    "PC2: Add appropriate ease allowance based on garment silhouette (fitted, semi-fitted, loose).",
                    "PC3: Draft balanced 2D paper patterns with darts, notches, and grain lines marked clearly.",
                    "PC4: Advise clients on suitable fabric selection, drape, texture, and trim compatibility."
                ],
                "viva_questions": [
                    "How much wearing ease is typically added to chest/bust measurement for a standard shirt/kurti?",
                    "What is the significance of the fabric grain line when drafting a sleeve?"
                ]
            },
            {
                "code": "AMH/N1948",
                "title": "Inspect, layout, mark, and cut fabric ensuring grainline alignment",
                "weight": 20,
                "keywords": ["fabric inspection", "shrinkage", "ironing", "marker layout", "selvedge", "grainline", "bias", "seam allowance", "shears", "notches", "fabric economy"],
                "performance_criteria": [
                    "PC1: Inspect fabric for weave flaws, dye patches, and pre-shrink cottons if necessary.",
                    "PC2: Lay pattern pieces on fabric matching straight grain with selvedge to prevent garment twisting.",
                    "PC3: Mark seam allowances (1.5cm side seam, 1cm armhole, 2.5cm hem) cleanly with tailor's chalk.",
                    "PC4: Cut multiple fabric layers cleanly along chalk lines using sharpened dressmaking shears."
                ],
                "viva_questions": [
                    "What causes a stitched trouser leg to twist while walking, and how is it prevented in cutting?",
                    "Why must printed or striped fabrics be laid with special matching techniques?"
                ]
            },
            {
                "code": "AMH/N1949",
                "title": "Operate sewing machine and assemble garment components",
                "weight": 30,
                "keywords": ["sewing machine", "lockstitch", "needle", "bobbin", "thread tension", "stitch length", "darts", "collar", "cuff", "zipper", "placket", "piping", "interfacing"],
                "performance_criteria": [
                    "PC1: Thread machine, adjust needle size (no. 11 for silk/chiffon, no. 14 for cotton, no. 16 for denim).",
                    "PC2: Balance upper and lower bobbin thread tension to achieve perfect lockstitches without loops.",
                    "PC3: Construct darts, attach fusible interfacing to collars, and stitch concealed zippers neatly.",
                    "PC4: Assemble sleeves and side seams with even seam margins without puckering or bunching."
                ],
                "viva_questions": [
                    "How do you diagnose and fix looped stitches appearing on the underside of fabric?",
                    "Which sewing needle number would you choose for stitching sheer georgette versus heavy denim?"
                ]
            },
            {
                "code": "AMH/N1950",
                "title": "Perform garment alterations, pressing, button-holing, and quality check",
                "weight": 15,
                "keywords": ["alteration", "hemming", "blind hem", "button", "buttonhole", "interfacing", "steam iron", "pressing", "thread trimming", "quality check", "loose threads"],
                "performance_criteria": [
                    "PC1: Perform client trial fitting and pin necessary alterations for waist or length adjustments.",
                    "PC2: Mark and execute uniform buttonholes and sew buttons with proper thread shank.",
                    "PC3: Trim all loose thread ends and perform final steam pressing to set sharp seams and creases.",
                    "PC4: Check final garment dimensions against original client specification sheet."
                ],
                "viva_questions": [
                    "Why is creating a thread shank important when sewing buttons on heavy coats or jackets?",
                    "What is the difference between pressing a seam and ironing fabric?"
                ]
            },
            {
                "code": "AMH/N1951",
                "title": "Maintain ergonomic workstation, needle safety, and equipment upkeep",
                "weight": 10,
                "keywords": ["needle safety", "broken needle policy", "machine oiling", "lint cleaning", "ergonomics", "chair posture", "scissor safety", "fire safety"],
                "performance_criteria": [
                    "PC1: Clean lint from shuttle race and feed dog and lubricate sewing machine mechanism daily.",
                    "PC2: Dispose broken machine needle fragments in designated magnetic container to prevent injury.",
                    "PC3: Maintain correct ergonomic sitting posture to prevent neck and back fatigue during long shifts.",
                    "PC4: Store cutting shears, pins, and rotary blades safely in protective sheaths."
                ],
                "viva_questions": [
                    "What is the standard procedure if a machine needle snaps during sewing?",
                    "How often should a commercial lockstitch sewing machine shuttle race be cleaned and oiled?"
                ]
            }
        ]
    }
}

# Helper trade list for forms
TRADE_OPTIONS = [
    {"id": "electrician", "name": "Domestic Electrician", "code": "ELE/Q6001", "sector": "Electronics & Power"},
    {"id": "plumber", "name": "General Plumber", "code": "PSC/Q0104", "sector": "Plumbing"},
    {"id": "mason", "name": "General Mason", "code": "CON/Q0102", "sector": "Construction"},
    {"id": "automotive", "name": "Two-Wheeler Service Technician", "code": "ASC/Q1411", "sector": "Automotive"},
    {"id": "welder", "name": "Manual Metal Arc Welder", "code": "CSC/Q0204", "sector": "Capital Goods"},
    {"id": "tailor", "name": "Self Employed Tailor", "code": "AMH/Q1947", "sector": "Apparel & Home Furnishing"}
]

# Curated sample experience descriptions for quick testing by hackathon evaluators
SAMPLE_EXPERIENCES = {
    "electrician": (
        "I have been working as an electrician for over 6 years in residential apartments and individual houses. "
        "My daily work includes reading house wiring blueprints, cutting wall chases for PVC conduits, and pulling phase, "
        "neutral, and earth wires. I size copper cables based on appliance wattage (1.5 sq mm for lighting, 4 sq mm for ACs). "
        "I assemble distribution boards with MCBs (6A to 32A) and install RCCBs to protect families from electric shock. "
        "I regularly install switchboards, ceiling fans with regulators, LED lights, and 16A sockets for water heaters. "
        "I also construct chemical earthing pits using bentonite compound and copper electrodes to ensure earth resistance "
        "remains below 3 ohms. I use a digital multimeter to check circuit continuity and voltage, and Megger to test insulation resistance. "
        "I always wear rubber-insulated safety boots and de-energize the main isolator before doing any wiring repair."
    ),
    "plumber": (
        "I have worked for 5 years as an independent plumber doing house installations and repair maintenance. "
        "I read plumbing layout drawings to plan pipe slopes for waste drainage so there is no clogging. "
        "I cut and join CPVC and UPVC pipes using solvent cement and primer, making sure joints dry properly before pressure testing. "
        "On high-pressure GI lines, I cut clean threads with a die and use Teflon tape and thread sealant to prevent water leaks. "
        "I have installed European water closets with dual-flush tanks, wall-hung wash basins with bottle traps, concealed shower diverters, "
        "and geysers with pressure relief safety valves. When customers have blockages, I use a drain snake auger to clear debris from traps. "
        "I always wear rubber gloves and safety boots when clearing sewage lines and take precautions against toxic gases."
    ),
    "mason": (
        "I have 7 years of hands-on experience in building construction as a mason. "
        "I prepare mortar mixtures in correct proportions such as 1:4 for brickwork and 1:6 for plastering, controlling the water-cement ratio. "
        "Before laying clay bricks, I soak them thoroughly in clean water tanks to avoid mortar dehydration. "
        "I construct strong English bond and Flemish bond walls, keeping all bed joints uniform at 10mm and checking perpends. "
        "I constantly check wall verticality using a plumb bob and verify horizontal courses with a water tube level and spirit level. "
        "For plastering, I set up reference bull marks to ensure an even 12mm thickness and fix chicken wire mesh across concrete-brick joints "
        "to prevent cracks. I instruct my team to cure walls twice daily with water for 10 days. I always wear a safety helmet and harness on scaffolding."
    ),
    "automotive": (
        "I have run my two-wheeler repair garage for 6 years servicing motorcycles and scooters from Hero, Bajaj, Honda, and Yamaha. "
        "In regular maintenance, I drain used engine oil, clean magnetic drain plugs, replace oil and air filters, and set spark plug gaps to 0.75mm using feeler gauges. "
        "I check and set valve tappet clearances to eliminate engine ticking noises and adjust chain slack between 20-30mm. "
        "I overhaul carburetors, ultrasonic clean jets, and on modern BS6 bikes I connect an OBD diagnostic scanner to read sensor fault codes. "
        "I inspect disc brake pads, bleed hydraulic brake lines using DOT4 brake fluid to remove spongy air bubbles, and replace fork oil seals. "
        "I test battery health with a digital multimeter and check stator charging output at 14.2V. I safely collect used engine oil in recycle barrels."
    ),
    "welder": (
        "I have been doing manual metal arc welding (SMAW) for 4 years in a structural fabrication workshop. "
        "Before welding, I bevel plate edges to a 60-degree V-groove using an angle grinder, clean rust with a wire brush, and set a 2.5mm root gap with spacers. "
        "I place solid tack welds at both ends of the joint. I select E6013 electrodes for light frames and low-hydrogen E7018 for structural joints. "
        "I set the welding machine amperage to 110A for 3.15mm electrodes and maintain a short, steady arc length with a 15-degree drag angle. "
        "After depositing each weld pass, I chip away slag with a chipping hammer, clean with a wire brush, and inspect for undercut or porosity. "
        "I check fillet throat thickness with a weld gauge. I always wear a DIN 11 auto-darkening welding helmet, chrome leather gloves, and keep a CO2 fire extinguisher nearby."
    ),
    "tailor": (
        "I have operated my tailoring boutique for 8 years making customized men's shirts, trousers, women's suits, and blouses. "
        "I take thorough client body measurements with a flexible tape and draft custom paper patterns with proper ease allowances (2.5 inches for shirts). "
        "I inspect fabric for defects, straighten grainlines against the selvedge, and mark accurate seam allowances with tailor's chalk before cutting with dressmaking shears. "
        "I operate a single-needle lockstitch sewing machine, selecting size 11 needles for fine silks and size 14 for cottons. "
        "I balance upper and lower bobbin tension to eliminate looped stitches. I construct sharp collars with fusible interfacing, insert concealed zippers, and stitch crisp darts. "
        "I do trial fittings, alter hems, hand-sew shank buttons, and finish garments with steam pressing. I oil my machine daily and store broken needles safely in a magnetic box."
    )
}
