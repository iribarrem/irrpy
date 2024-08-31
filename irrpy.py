import click
import json
import logging
import subprocess
from ipaddress import ip_network, IPv4Network, IPv6Network
from typing import Dict, List, Union

@click.command()
@click.version_option(version="0.1", prog_name="IRRpy")
@click.argument("as_sets", nargs=-1, type=str)
@click.option("--ip_family", "-f", 
              help="Query only one IP Family (4, 6)",
              nargs=1, required=False, default=None, type=int
)
@click.option("--depth", "-d", 
              help="How deep should AS-SET cone be searched", 
              nargs=1, required=False, default=None, type=int
)
def get_irr_prefixes(
    as_sets: Union[str, list[str]], 
    ip_family: Union[int, None]=None, 
    depth: Union[int, None]=None
) -> Dict: # type: ignore
    """
    Get prefixes from IRR Route Objects for given AS's or AS-SETs, including downstream AS's/AS-SETs
    """
    
    log = logging.getLogger(__name__)
    log.info(f"Searching IRR Route Objects for AS-SETs {as_sets}")
    
    if ip_family not in [None, 4, 6]:
        raise ValueError(f"Value {ip_family} is not a valid IP Family, must be None(both), 4 or 6")
    
    if isinstance(as_sets, str):
        as_sets = [as_sets]
    
    for as_set in as_sets:
        cmd_ipv4: str = f"bgpq4 -4j{f" -L {depth}" if depth else ""} -l prefixes {as_set}"
        cmd_ipv6: str = f"bgpq4 -6j{f" -L {depth}" if depth else ""} -l prefixes {as_set}"
        log.debug(cmd_ipv4)
        log.debug(cmd_ipv6)
        commands: List[List[str]] = []
        
        if not ip_family:
            log.info("Searching both IPv4 and IPv6 route objects")
            commands.append(cmd_ipv4.split(" "))
            commands.append(cmd_ipv6.split(" "))
        elif ip_family == 4:
            log.info("Searching only IPv4 route objects")
            commands.append(cmd_ipv4.split(" "))
        else:
            log.info("Searching only IPv6 route objects")
            commands.append(cmd_ipv6.split(" "))
        
        results: List = []    
        for cmd in commands:
            log.debug(f"Running command: {cmd}")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            log.debug(f"Command output: {output}")
            log.debug(f"Command error: {error}")
            
            results.append(json.loads(output.decode("ascii")))

        response: Dict = {
            "ipv4": [],
            "ipv6": []
        }
        for result in results:
            for prefix in result["prefixes"]:
                prefix = prefix["prefix"]
                try:
                    prefix_obj = ip_network(prefix)
                except:
                    raise ValueError(f"Prefix {prefix} returned by BGPq4 is not a valid IP subnet.")

                if isinstance(prefix_obj, IPv4Network):
                    response["ipv4"].append(prefix)
                elif isinstance(prefix_obj, IPv6Network):
                    response["ipv6"].append(prefix)
        
        log.debug(f"Return: {response}")
        
        return response
    
if __name__ == "__main__":
    get_irr_prefixes()