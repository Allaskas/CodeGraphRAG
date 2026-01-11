from typing import Dict, Set, Any
from .base_strategy import BaseAntipatternStrategy
from .utils import find_related_files_by_relationships, find_node_by_entity_location_and_file


class MHStrategy(BaseAntipatternStrategy):

    def find_direct_related_files(self, graph_data: Dict, antipattern_json: Dict) -> Set[str]:
        files: Set[str] = set()

        def extract_files(obj: Any):
            if isinstance(obj, dict):
                for value in obj.values():
                    extract_files(value)
            elif isinstance(obj, list):
                for item in obj:
                    extract_files(item)
            elif isinstance(obj, str):
                if obj.endswith(".java"):
                    files.add(obj)

        extract_files(antipattern_json)
        return files

    def find_indirect_related_files(self, graph_data: Dict, antipattern_json: Dict) -> Set[str]:
        """
        Find indirect related files starting from antipattern start/end nodes
        """
        start_end_nodes = []

        for key in ("start", "end"):
            node_info = antipattern_json.get(key)
            if not node_info:
                continue

            entity = node_info.get("object")
            location = node_info.get("location")
            file_path = node_info.get("file")

            if not entity or not location or not file_path:
                continue

            start_end_nodes.append({
                "entity": entity,
                "location": location,
                "file": file_path
            })

        start_node_ids: Set[int] = set()

        for item in start_end_nodes:
            node = find_node_by_entity_location_and_file(
                graph_data,
                entity=item["entity"],
                location=item["location"],
                file_path=item["file"]
            )
            if not node:
                continue

            node_id = node.get("properties", {}).get("id") or node.get("node_id")
            if node_id:
                start_node_ids.add(node_id)

        all_indirect: Set[str] = set()

        if start_node_ids:
            all_indirect = find_related_files_by_relationships(
                graph_data,
                node_ids=start_node_ids
            )

        all_direct = self.find_direct_related_files(graph_data, antipattern_json)

        return all_indirect - all_direct
