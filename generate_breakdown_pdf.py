#!/usr/bin/env python3
"""Generate a PDF breakdown of the SNMPeek program."""

from fpdf import FPDF


class BreakdownPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, "SNMPeek - Program Breakdown", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(50, 100, 180)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(140, 140, 140)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, num, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 70, 150)
        self.cell(0, 10, f"{num}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(30, 70, 150)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 120, self.get_y())
        self.ln(3)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(60, 60, 60)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def code_block(self, code):
        self.set_font("Courier", "", 8.5)
        self.set_fill_color(240, 240, 245)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.set_x(x + 4)
        self.multi_cell(180, 4.5, code, fill=True)
        self.set_x(x)
        self.ln(2)

    def bullet(self, text, indent=14):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        x = self.get_x()
        self.set_x(x + indent)
        # bullet char
        self.set_font("ZapfDingbats", "", 6)
        self.cell(5, 5.5, "l")  # small bullet in ZapfDingbats
        self.set_font("Helvetica", "", 10)
        self.multi_cell(170 - indent, 5.5, text)
        self.set_x(x)

    def key_value(self, key, value, indent=14):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        x = self.get_x()
        self.set_x(x + indent)
        self.set_font("Helvetica", "B", 10)
        self.cell(self.get_string_width(key + ": ") + 2, 5.5, f"{key}: ")
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, value)
        self.set_x(x)


def build_pdf():
    pdf = BreakdownPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ===== TITLE PAGE =====
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(30, 70, 150)
    pdf.cell(0, 15, "SNMPeek", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, "Complete Program Breakdown", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(5)
    pdf.set_draw_color(30, 70, 150)
    pdf.set_line_width(0.5)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 6, (
        "SNMPeek is a CLI tool that queries an AKiPS network monitoring server to look up "
        "network devices by CIDR subnet, hostname pattern, or MAC address. It displays results "
        "in rich terminal tables and optionally exports to CSV."
    ), align="C")

    pdf.ln(15)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 70, 150)
    pdf.cell(0, 8, "Table of Contents", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    toc = [
        "1. Imports & Global Setup",
        "2. MAC Address Utilities",
        "3. Argument Parsing",
        "4. Query Classification",
        "5. AKiPS Connection",
        "6. Data Fetching",
        "7. Enum State Parsing",
        "8. Uptime Formatting",
        "9. Device Filtering & Merging",
        "10. Rich Table Display",
        "11. CSV Export",
        "12. Switch Port Mapper (SPM) Functions",
        "13. MAC Data Fetching & Enrichment",
        "14. MAC Results Display",
        "15. MAC CSV Export",
        "16. Main Entry Point & Orchestration",
        "17. Program Flow Diagram",
    ]
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    for item in toc:
        pdf.cell(0, 6, f"    {item}", new_x="LMARGIN", new_y="NEXT")

    # ===== SECTION 1 =====
    pdf.add_page()
    pdf.section_title("1", "Imports & Global Setup  (Lines 1-33)")

    pdf.sub_title("Purpose")
    pdf.body_text(
        "Sets up the runtime environment: the shebang line points to the project's virtual "
        "environment Python, standard library and third-party modules are imported, and "
        "global constants are initialized."
    )

    pdf.sub_title("Step-by-Step")
    pdf.bullet("Line 1 (Shebang): #!/home/tuna/.../. venv/bin/python tells the OS to run this script with the project's virtual environment Python, ensuring all installed packages are available.")
    pdf.bullet("Lines 4-11 (Stdlib imports): argparse (CLI parsing), csv (CSV export), fnmatch (wildcard hostname matching), ipaddress (CIDR/IP validation), os (env vars), re (regex), sys (exit codes), datetime (timestamps).")
    pdf.bullet("Lines 13-18 (Third-party imports): akips.AKIPS (AKiPS API client), dotenv.load_dotenv (.env file loader), rich.Console/Panel/Table/Text (terminal formatting).")
    pdf.bullet("Line 20: console = Console() creates a single Rich console instance used throughout the program for styled output and status spinners.")
    pdf.bullet("Lines 24-33 (MAC_PATTERN): A compiled regex that matches all common MAC address formats: colon-separated (AA:BB:CC:DD:EE:FF), dash-separated (AA-BB-CC-DD-EE-FF), dot-quad (AABB.CCDD.EEFF), dash-quad (AABB-CCDD-EEFF), and bare hex (AABBCCDDEEFF). Case-insensitive via character classes.")

    # ===== SECTION 2 =====
    pdf.section_title("2", "MAC Address Utilities  (Lines 36-75)")

    pdf.sub_title("normalize_mac(mac_str)  -  Lines 36-43")
    pdf.body_text(
        "Converts any MAC format to a canonical colon-separated lowercase form."
    )
    pdf.bullet("Step 1: Strip all non-hex characters using re.sub(r\"[^0-9a-fA-F]\", \"\", mac_str) and lowercase the result.")
    pdf.bullet("Step 2: If no hex characters remain, return the lowered original string.")
    pdf.bullet("Step 3: Re-join hex chars in pairs with colons: \"aabbccddeeff\" becomes \"aa:bb:cc:dd:ee:ff\".")

    pdf.sub_title("is_partial_mac(s)  -  Lines 46-75")
    pdf.body_text(
        "Detects partial MAC addresses (fewer than 6 octets) that still look MAC-like. "
        "Requires at least one delimiter character to avoid false positives on short "
        "hex strings like hostnames."
    )
    pdf.bullet("Checks colon-separated partial: e.g. \"aa:bb:cc\" (2-5 octets).")
    pdf.bullet("Checks dash-separated partial: e.g. \"aa-bb-cc\".")
    pdf.bullet("Checks dot-quad partial: e.g. \"aabb.ccdd\" (HPE format).")
    pdf.bullet("Checks dash-quad partial: e.g. \"aabb-ccdd\".")
    pdf.bullet("Returns True if any pattern matches, False otherwise.")

    # ===== SECTION 3 =====
    pdf.section_title("3", "Argument Parsing  (Lines 78-149)")

    pdf.sub_title("parse_args()")
    pdf.body_text(
        "Defines and processes all CLI arguments using argparse."
    )

    pdf.sub_title("Positional Argument")
    pdf.bullet("query (nargs=\"+\"): One or more queries. Can be CIDR subnets (10.1.0.0/24), MAC addresses (aa:bb:cc:dd:ee:ff), or hostname patterns (*switch*). Multiple queries can be mixed.")

    pdf.sub_title("Optional Field Flags")
    pdf.bullet("-g / --groups: Include AKiPS group memberships in output.")
    pdf.bullet("-d / --descr: Include sysDescr (OS/model info) in output.")
    pdf.bullet("--location: Include sysLocation in output.")
    pdf.bullet("-l / --lldp: Include LLDP neighbor discovery data in output.")
    pdf.bullet("--snmp: Include SNMP reachability state in output.")
    pdf.bullet("-a / --all-fields: Shortcut to enable ALL optional fields at once.")

    pdf.sub_title("Output Options")
    pdf.bullet("-o / --output FILE: Write CSV to a specific filename (implies --csv).")
    pdf.bullet("--csv: Enable CSV export with an auto-generated filename.")

    pdf.sub_title("Post-Processing Logic")
    pdf.bullet("If -o is provided, args.csv is auto-set to True.")
    pdf.bullet("If --all-fields is set, all individual field flags (groups, descr, location, lldp, snmp) are set to True.")

    # ===== SECTION 4 =====
    pdf.add_page()
    pdf.section_title("4", "Query Classification  (Lines 152-177)")

    pdf.sub_title("classify_query(query_str)")
    pdf.body_text(
        "Determines the type of each user-provided query string and returns a "
        "(type, normalized_value) tuple. This is the core routing logic."
    )
    pdf.bullet("Step 1: Strip whitespace. Test against MAC_PATTERN for full MAC addresses.")
    pdf.bullet("Step 2: Test with is_partial_mac() for partial MAC addresses.")
    pdf.bullet("Step 3: If MAC matched, return (\"mac\", normalize_mac(stripped)).")
    pdf.bullet("Step 4: Try ipaddress.ip_network(query_str, strict=False). If valid, return (\"subnet\", network). The strict=False flag allows host-bits to be set (e.g. 10.1.0.5/24 is treated as 10.1.0.0/24).")
    pdf.bullet("Step 5: If not a MAC or subnet, treat as hostname pattern. If no wildcards (* or ?) are present, automatically wrap in wildcards: \"switch\" becomes \"*switch*\" for substring matching.")
    pdf.bullet("Returns (\"hostname\", pattern).")

    # ===== SECTION 5 =====
    pdf.section_title("5", "AKiPS Connection  (Lines 180-210)")

    pdf.sub_title("connect_akips()")
    pdf.body_text("Initializes the AKiPS API client from environment variables.")
    pdf.bullet("Step 1: Call load_dotenv() to load variables from the .env file in the project root.")
    pdf.bullet("Step 2: Read environment variables:")
    pdf.key_value("AKIPS_SERVER", "Required. The hostname/IP of the AKiPS server.")
    pdf.key_value("AKIPS_USERNAME", "Defaults to \"api-ro\" (read-only API user).")
    pdf.key_value("AKIPS_PASSWORD", "Required. The API password.")
    pdf.key_value("AKIPS_VERIFY_SSL", "Defaults to \"true\". Set to \"false\" to skip SSL verification.")
    pdf.key_value("AKIPS_TIMEZONE", "Defaults to \"America/Los_Angeles\".")
    pdf.bullet("Step 3: If AKIPS_SERVER or AKIPS_PASSWORD is missing, print an error message and exit with code 1.")
    pdf.bullet("Step 4: Create and return an AKIPS client object initialized with all credentials.")

    # ===== SECTION 6 =====
    pdf.section_title("6", "Data Fetching  (Lines 214-242)")

    pdf.sub_title("fetch_data(api, args)")
    pdf.body_text(
        "Retrieves device data and optional enrichment data from AKiPS. Each API call "
        "displays a Rich spinner while running."
    )
    pdf.bullet("Step 1 (Always): Fetch all devices via api.get_devices(). Returns a dict of {device_name: {attribute: value}}.")
    pdf.bullet("Step 2 (Always): Fetch ICMP ping states via api.get_attributes(attribute=\"PING.icmpState\"). Used to determine up/down status and uptime.")
    pdf.bullet("Step 3 (If --groups): Fetch group memberships via api.get_group_membership().")
    pdf.bullet("Step 4 (If --snmp): Fetch SNMP states via api.get_attributes(attribute=\"SNMP.snmpState\").")
    pdf.bullet("Step 5 (If --lldp): Fetch LLDP neighbor data using a regex attribute filter that matches both lldpRemSysName and lldpRemPortId.")
    pdf.bullet("Returns tuple: (devices, ping_states, extras_dict).")

    # ===== SECTION 7 =====
    pdf.add_page()
    pdf.section_title("7", "Enum State Parsing  (Lines 245-266)")

    pdf.sub_title("parse_enum_state(enum_data)")
    pdf.body_text(
        "Parses AKiPS enum strings. SNMP enumerated types (like interface status) are "
        "stored by AKiPS as comma-delimited strings with 5 fields:"
    )
    pdf.code_block("Format: number,value,created,modified,description\nExample: 1,up,1700000000,1707000000,Interface is operational")
    pdf.bullet("Step 1: Guard clause - return (None, None) if enum_data is empty.")
    pdf.bullet("Step 2: Apply regex with 5 capture groups matching non-whitespace fields separated by commas (the description field can contain spaces).")
    pdf.bullet("Step 3: Extract group 2 as the value (e.g. \"up\", \"down\").")
    pdf.bullet("Step 4: Parse group 4 as a Unix epoch timestamp and convert to a datetime object. If parsing fails, set modified to None.")
    pdf.bullet("Step 5: Return (value, modified_datetime).")
    pdf.body_text("Note: Line 253 contains a debug print(modified) statement that should be removed for production use.")

    # ===== SECTION 8 =====
    pdf.section_title("8", "Uptime Formatting  (Lines 269-282)")

    pdf.sub_title("format_uptime(delta)")
    pdf.body_text("Converts a timedelta object into a human-readable uptime string.")
    pdf.bullet("Step 1: Convert to total seconds. If negative, return \"N/A\".")
    pdf.bullet("Step 2: Use divmod to break into days, hours, minutes.")
    pdf.bullet("Step 3: Format contextually:")
    pdf.key_value("Days present", "\"5d 3h 22m\"")
    pdf.key_value("Hours only", "\"3h 22m\"")
    pdf.key_value("Minutes only", "\"22m\"")

    # ===== SECTION 9 =====
    pdf.section_title("9", "Device Filtering & Merging  (Lines 285-388)")

    pdf.sub_title("filter_and_merge(networks, hostname_patterns, devices, ping_states, extras, args)")
    pdf.body_text(
        "The core data processing function. Iterates all devices, applies filters, "
        "extracts status info, and builds result rows. This is where raw AKiPS data "
        "becomes structured output."
    )

    pdf.sub_title("Filtering Phase (Lines 293-315)")
    pdf.bullet("For each device, parse its IPv4 address with ipaddress.ip_address().")
    pdf.bullet("Check if the IP falls within ANY of the provided subnets (using Python's \"ip in network\" operator).")
    pdf.bullet("If no subnet match, check if hostname or device_name matches ANY hostname pattern (case-insensitive fnmatch wildcard matching).")
    pdf.bullet("If neither matches, skip the device entirely.")

    pdf.sub_title("Status Extraction Phase (Lines 317-336)")
    pdf.bullet("Look up the device in ping_states data.")
    pdf.bullet("Parse the PING.icmpState enum value using parse_enum_state().")
    pdf.bullet("If value is \"up\": status = \"Active\", last_seen = now, uptime = now - modified_time.")
    pdf.bullet("If value is anything else: status = \"Inactive\", last_seen = modified_time.")
    pdf.bullet("If no ping data found: status remains \"Unknown\".")

    pdf.sub_title("Row Building Phase (Lines 338-382)")
    pdf.bullet("Build a base row dict with: hostname, ip, status, uptime, last_seen, _ip_obj (for sorting).")
    pdf.bullet("Conditionally add optional fields based on CLI flags:")
    pdf.key_value("--descr", "SNMPv2-MIB.sysDescr from device attributes")
    pdf.key_value("--location", "SNMPv2-MIB.sysLocation from device attributes")
    pdf.key_value("--groups", "Group list from extras[\"groups\"] data")
    pdf.key_value("--snmp", "SNMP state parsed from extras[\"snmp\"] enum data")
    pdf.key_value("--lldp", "LLDP neighbors assembled from lldpRemSysName + lldpRemPortId")

    pdf.sub_title("Sorting (Line 387)")
    pdf.bullet("Sort all results by IP address (ascending). Devices without IPs sort to 0.0.0.0.")

    # ===== SECTION 10 =====
    pdf.add_page()
    pdf.section_title("10", "Rich Table Display  (Lines 391-484)")

    pdf.sub_title("display_results(results, networks, hostname_patterns, args)")
    pdf.body_text("Renders the filtered results as a styled terminal table using the Rich library.")

    pdf.sub_title("Summary Panel (Lines 393-413)")
    pdf.bullet("Count Active, Inactive, and Unknown devices.")
    pdf.bullet("Build a styled Rich Text object showing: query parameters, total found, active (green), inactive (red), unknown (yellow).")
    pdf.bullet("Display inside a Rich Panel with blue border, titled \"AKIPS Host Query\".")

    pdf.sub_title("Table Construction (Lines 418-484)")
    pdf.bullet("Create a Rich Table with alternating row styles (plain / grey background) for readability.")
    pdf.bullet("Default columns: Hostname (cyan), IP Address, Status (colored indicator), Uptime (green if active), Last Seen.")
    pdf.bullet("Optional columns added dynamically based on CLI flags: Description, Location, Groups, SNMP, LLDP Neighbors.")
    pdf.bullet("Status rendering: green circle + \"Active\", red circle + \"Inactive\", yellow circle + \"Unknown\".")
    pdf.bullet("Uptime uses format_uptime() helper; shows \"N/A\" in dim style if unavailable.")

    # ===== SECTION 11 =====
    pdf.section_title("11", "CSV Export  (Lines 487-527)")

    pdf.sub_title("write_csv(results, filename, args)")
    pdf.body_text("Writes the same data shown in the terminal table to a CSV file.")
    pdf.bullet("Step 1: Open file with csv.writer. Build header row with default + optional field names.")
    pdf.bullet("Step 2: For each result row, format uptime and last_seen as strings.")
    pdf.bullet("Step 3: Append optional field values (description, location, groups as comma-joined, SNMP state, LLDP neighbors as comma-joined).")
    pdf.bullet("Step 4: Write each row to the CSV.")

    # ===== SECTION 12 =====
    pdf.section_title("12", "Switch Port Mapper Functions  (Lines 533-619)")

    pdf.sub_title("query_spm(api, mac, ip)  -  Lines 533-545")
    pdf.body_text("Queries the AKiPS Switch Port Mapper (SPM) API endpoint.")
    pdf.bullet("Builds a params dict from optional mac/ip arguments.")
    pdf.bullet("Calls api._get(section=\"api-spm\") with a 30-second timeout.")
    pdf.bullet("Returns raw text response, or None on error (prints a warning).")

    pdf.sub_title("parse_spm_response(text)  -  Lines 548-619")
    pdf.body_text(
        "Parses the raw SPM API text response into a list of dicts. Handles variable "
        "formats since AKiPS SPM output is not strictly standardized."
    )
    pdf.bullet("Step 1: Detect delimiter by checking for tab, semicolon, or defaulting to comma.")
    pdf.bullet("Step 2: Detect if the first line is a header row by counting known keywords (mac, vendor, switch, interface, vlan, ip). If 2+ match, treat as headers.")
    pdf.bullet("Step 3a (With headers): Map header names to canonical keys (e.g. \"manufacturer\" -> \"vendor\", \"port\" -> \"interface\"). Parse each subsequent line into a dict.")
    pdf.bullet("Step 3b (Without headers): Assume positional field order: mac, vendor, switch, interface, vlan, ip.")
    pdf.bullet("Returns a list of entry dicts.")

    # ===== SECTION 13 =====
    pdf.add_page()
    pdf.section_title("13", "MAC Data Fetching & Enrichment  (Lines 622-686)")

    pdf.sub_title("fetch_mac_data(api, mac_addresses)")
    pdf.body_text(
        "Orchestrates MAC lookups: queries SPM, then enriches each result with "
        "detailed port information from the switch."
    )

    pdf.sub_title("SPM Query Phase")
    pdf.bullet("For each MAC address, call query_spm() and parse the response with parse_spm_response().")

    pdf.sub_title("Port Enrichment Phase")
    pdf.bullet("For each SPM entry that has a switch + interface:")
    pdf.bullet("Query the switch for port attributes using a regex filter matching: ifOperStatus, ifAlias, ifHighSpeed, ifAdminStatus.")
    pdf.key_value("ifOperStatus", "Parsed as enum -> port_status (up/down) + port_last_change timestamp")
    pdf.key_value("ifAdminStatus", "Parsed as enum -> admin_status (up/down, distinguishes admin-shutdown)")
    pdf.key_value("ifAlias", "Port description label -> port_descr")
    pdf.key_value("ifHighSpeed", "Port speed in Mbps -> port_speed")

    pdf.sub_title("Event History Phase")
    pdf.bullet("Query api.get_events() for the switch/interface over the last 7 days.")
    pdf.bullet("Store up to 20 most recent events for display in the port history table.")

    pdf.sub_title("Return Structure")
    pdf.bullet("Returns a list of dicts, each containing: query_mac, entries (enriched list), raw (original SPM text).")

    # ===== SECTION 14 =====
    pdf.section_title("14", "MAC Results Display  (Lines 694-798)")

    pdf.sub_title("format_speed(speed_raw)  -  Lines 694-703")
    pdf.bullet("Converts Mbps integer to human-readable: 1000 -> \"1G\", 100 -> \"100M\".")

    pdf.sub_title("display_mac_results(mac_data_list)  -  Lines 706-798")
    pdf.body_text("Renders MAC lookup results with two tables per query.")

    pdf.sub_title("Summary Panel")
    pdf.bullet("Shows the queried MAC address and number of results found, in a magenta-bordered panel.")

    pdf.sub_title("Main Results Table")
    pdf.bullet("Columns: MAC Address, Vendor, IP Address, Switch, Port, VLAN, Port Status, Speed, Description.")
    pdf.bullet("Port status color-coded: green (up), red (down), yellow (admin down), dim (unknown).")

    pdf.sub_title("Event History Table")
    pdf.bullet("Only shown if events were found. Green-bordered table with columns: Time, Switch, Port, Type, Details.")
    pdf.bullet("Timestamps converted from Unix epoch to human-readable format.")

    # ===== SECTION 15 =====
    pdf.section_title("15", "MAC CSV Export  (Lines 801-828)")

    pdf.sub_title("write_mac_csv(mac_data_list, filename)")
    pdf.body_text("Writes MAC lookup results to CSV with 12 columns.")
    pdf.bullet("Headers: Query MAC, MAC Address, Vendor, IP Address, Switch, Port, VLAN, Port Status, Admin Status, Speed (Mbps), Port Description, Port Last Change.")
    pdf.bullet("Iterates all entries across all MAC queries and writes one row per SPM entry.")

    # ===== SECTION 16 =====
    pdf.add_page()
    pdf.section_title("16", "Main Entry Point  (Lines 831-920)")

    pdf.sub_title("main()")
    pdf.body_text(
        "The orchestrator function that ties everything together. Handles the complete "
        "program lifecycle from argument parsing to output."
    )

    pdf.sub_title("Phase 1: Argument Parsing & Classification (Lines 832-849)")
    pdf.bullet("Call parse_args() to get CLI arguments.")
    pdf.bullet("Initialize three empty lists: networks, hostname_patterns, mac_addresses.")
    pdf.bullet("For each query string, call classify_query() and route the result to the appropriate list.")

    pdf.sub_title("Phase 2: API Connection (Line 852)")
    pdf.bullet("Call connect_akips() to initialize the API client. Exits on credential errors.")

    pdf.sub_title("Phase 3: MAC Address Processing (Lines 856-873)")
    pdf.bullet("If mac_addresses is non-empty, call fetch_mac_data() to query the SPM endpoint.")
    pdf.bullet("Display results with display_mac_results().")
    pdf.bullet("If --csv is enabled, generate filename (from MAC hex digits) and call write_mac_csv().")
    pdf.bullet("On error: print error and exit only if there are no subnet/hostname queries to fall back to.")

    pdf.sub_title("Phase 4: Subnet/Hostname Processing (Lines 876-920)")
    pdf.bullet("If networks or hostname_patterns is non-empty, call fetch_data() to retrieve device/state data.")
    pdf.bullet("Call filter_and_merge() to apply filters and build result rows.")
    pdf.bullet("Call display_results() to render the Rich table.")
    pdf.bullet("If --csv is enabled, generate filename (from subnet/pattern labels) and call write_csv().")

    pdf.sub_title("Phase 5: Entry Guard (Lines 922-923)")
    pdf.bullet("if __name__ == \"__main__\": main() ensures the script only runs when executed directly, not when imported.")

    # ===== SECTION 17 =====
    pdf.section_title("17", "Program Flow Diagram")
    pdf.body_text("High-level execution flow when a user runs SNMPeek:")

    pdf.code_block(
        "User runs: ./SNMPeek 10.1.0.0/24 *switch* aa:bb:cc:dd:ee:ff -a --csv\n"
        "\n"
        "  1. parse_args()\n"
        "     +-- Parse CLI arguments\n"
        "     +-- --all-fields -> enable all optional field flags\n"
        "     +-- --csv -> enable CSV export\n"
        "\n"
        "  2. classify_query() x3\n"
        "     +-- \"10.1.0.0/24\"         -> (\"subnet\", IPv4Network)\n"
        "     +-- \"*switch*\"            -> (\"hostname\", \"*switch*\")\n"
        "     +-- \"aa:bb:cc:dd:ee:ff\"  -> (\"mac\", \"aa:bb:cc:dd:ee:ff\")\n"
        "\n"
        "  3. connect_akips()\n"
        "     +-- Load .env credentials\n"
        "     +-- Return AKIPS API client\n"
        "\n"
        "  4. MAC Path (if mac_addresses):\n"
        "     +-- fetch_mac_data()\n"
        "     |   +-- query_spm() -> parse_spm_response()\n"
        "     |   +-- Enrich with port attrs (ifOperStatus, etc.)\n"
        "     |   +-- Fetch 7-day event history\n"
        "     +-- display_mac_results()\n"
        "     +-- write_mac_csv() [if --csv]\n"
        "\n"
        "  5. Subnet/Hostname Path (if networks or hostname_patterns):\n"
        "     +-- fetch_data()\n"
        "     |   +-- get_devices()\n"
        "     |   +-- get_attributes(PING.icmpState)\n"
        "     |   +-- [optional] get_group_membership()\n"
        "     |   +-- [optional] get_attributes(SNMP.snmpState)\n"
        "     |   +-- [optional] get_attributes(LLDP-MIB.*)\n"
        "     +-- filter_and_merge()\n"
        "     |   +-- Match devices against subnets/patterns\n"
        "     |   +-- Parse ping state -> status/uptime\n"
        "     |   +-- Build enriched row dicts\n"
        "     |   +-- Sort by IP address\n"
        "     +-- display_results()\n"
        "     +-- write_csv() [if --csv]"
    )

    return pdf


if __name__ == "__main__":
    pdf = build_pdf()
    output_path = "/home/tuna/Documents/coding/SNMPeek/SNMPeek_Breakdown.pdf"
    pdf.output(output_path)
    print(f"PDF saved to: {output_path}")
