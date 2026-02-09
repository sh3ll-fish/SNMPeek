# SNMPeek

A command-line tool for querying [AKiPS](https://www.akips.com/) network monitoring servers. SNMPeek auto-detects query types and returns formatted device information, Switch Port Mapper lookups, and historical event data directly in the terminal.

## Features

- **Smart query detection** — automatically classifies input as CIDR subnet, IP address, MAC address (full or partial), or hostname pattern
- **MAC address lookups** via the AKiPS Switch Port Mapper (`api-spm`), with port enrichment and 7-day event history
- **Device queries** by subnet or hostname with ping status, uptime, LLDP neighbors, SNMP state, group memberships, and more
- **Rich terminal output** — color-coded tables with status indicators
- **CSV export** — optional export for further analysis or reporting
- **Multiple queries** in a single invocation, including mixed types

## Requirements

- Python 3.10+
- Access to an AKiPS server with the `api-db` Web API section enabled
- `api-spm` section enabled on AKiPS for MAC address lookups

## Installation

```bash
git clone https://github.com/sh3ll-fish/SNMPeek.git
cd SNMPeek

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy the example environment file and fill in your AKiPS credentials:

```bash
cp .env.example .env
```

```ini
AKIPS_SERVER=akips.example.com
AKIPS_USERNAME=api-ro
AKIPS_PASSWORD=changeme
AKIPS_VERIFY_SSL=true
AKIPS_TIMEZONE=America/New_York
```

## Usage

```
./SNMPeek_APIKips [OPTIONS] QUERY [QUERY ...]
```

The tool auto-detects what kind of query you're running:

| Input | Detected As | Example |
|---|---|---|
| CIDR notation | Subnet scan | `10.1.0.0/24` |
| IP address | Single host | `192.168.1.1` |
| MAC address | SPM lookup | `aa:bb:cc:dd:ee:ff` |
| Partial MAC | SPM lookup | `00:50:56`, `aabb.ccdd` |
| Anything else | Hostname pattern | `switch-core`, `*router*` |

Plain hostname strings are automatically wrapped as substring matches (`switch` becomes `*switch*`).

### Examples

Query a subnet:

```bash
./SNMPeek_APIKips 10.1.0.0/24
```

Search by hostname pattern with all optional fields:

```bash
./SNMPeek_APIKips -a "*core-sw*"
```

Look up a MAC address:

```bash
./SNMPeek_APIKips aa:bb:cc:dd:ee:ff
```

Search by vendor OUI (partial MAC):

```bash
./SNMPeek_APIKips 00:50:56
```

Mixed query — MAC lookup and subnet scan in one command:

```bash
./SNMPeek_APIKips aa:bb:cc:dd:ee:ff 10.1.0.0/24
```

Export results to CSV:

```bash
./SNMPeek_APIKips --csv 10.1.0.0/24
./SNMPeek_APIKips -o results.csv "*switch*"
```

### Options

```
positional arguments:
  query                CIDR subnet, MAC address, or hostname pattern
                       (can pass multiple)

options:
  -h, --help           Show help message and exit
  --csv                Export results to a CSV file
  -o, --output FILE    Write CSV to FILE (implies --csv)

optional fields:
  -g, --groups         Show group memberships
  -d, --descr          Show system description (OS/model)
  --location           Show sysLocation
  -l, --lldp           Show LLDP neighbor info
  --snmp               Show SNMP reachability state
  -a, --all-fields     Show all optional fields
```

## MAC Address Formats

All common formats are accepted (case-insensitive) and normalized internally:

| Format | Example |
|---|---|
| Colon-separated | `AA:BB:CC:DD:EE:FF` |
| Dash-separated | `AA-BB-CC-DD-EE-FF` |
| Cisco dot notation | `AABB.CCDD.EEFF` |
| Dash groups of four | `AABB-CCDD-EEFF` |
| Plain hex | `AABBCCDDEEFF` |
| Partial (with delimiter) | `00:50:56`, `AABB.CC`, `00-50-56` |

## Output

### Host Query (Subnet / Hostname)

Displays a summary panel with match counts and a table with:

- Hostname, IP Address, Status (Active/Inactive/Unknown), Uptime, Last Seen
- Optional: Description, Location, Groups, SNMP State, LLDP Neighbors

### MAC Lookup

Displays SPM results enriched with live port data:

- MAC Address, Vendor, IP Address, Switch, Port, VLAN
- Port Status, Speed, Interface Description
- 7-day port event history (link up/down events)

### CSV

CSV export is off by default. Use `--csv` for an auto-named file or `-o FILE` to specify the path.

## AKiPS Server Configuration

The following Web API sections should be enabled on your AKiPS server (under Web API Settings):

| Section | Purpose |
|---|---|
| `api-db` | Device data, ping/SNMP states, LLDP, groups, events |
| `api-spm` | Switch Port Mapper for MAC lookups |

The tool connects using the `api-ro` read-only user by default. No write access is required.

## Documentation

A full technical reference covering the internal process flow, data pipelines, and architecture is included:

- [`SNMPeek_Technical_Reference.pdf`](SNMPeek_Technical_Reference.pdf) — printable PDF
- [`SNMPeek_Technical_Reference.md`](SNMPeek_Technical_Reference.md) — source markdown

## License

Internal tool — Oregon State University.
