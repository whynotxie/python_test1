"""Simple Verilog writer utility.

Provides `VerilogModule` to programmatically construct a Verilog module
and emit its textual representation to a file.

Usage example in `verilog_writer_example.py`.
"""
from typing import List, Tuple, Dict, Optional


def _width_str(width: int) -> str:
    return f"[{width-1}:0] " if width and width > 1 else ""


class VerilogModule:
    def __init__(self, name: str):
        self.name = name
        self.ports: List[Tuple[str, str, int]] = []  # (name, dir, width)
        self.parameters: List[Tuple[str, Optional[str]]] = []  # (name, default)
        self.wires: List[Tuple[str, int]] = []
        self.regs: List[Tuple[str, int]] = []
        self.assigns: List[Tuple[str, str]] = []
        self.always_blocks: List[Tuple[str, List[str]]] = []  # (sensitivity, body_lines)
        self.instances: List[Tuple[str, str, Dict[str, str], Dict[str, str]]] = []

    def add_parameter(self, name: str, default: Optional[str] = None):
        self.parameters.append((name, default))

    def add_port(self, name: str, direction: str = "input", width: int = 1):
        self.ports.append((name, direction, width))

    def add_wire(self, name: str, width: int = 1):
        self.wires.append((name, width))

    def add_reg(self, name: str, width: int = 1):
        self.regs.append((name, width))

    def add_assign(self, lhs: str, rhs: str):
        self.assigns.append((lhs, rhs))

    def add_always(self, sensitivity: str, body_lines: List[str]):
        self.always_blocks.append((sensitivity, body_lines))

    def add_instance(self, module: str, inst_name: str, params: Dict[str, str], conns: Dict[str, str]):
        """Add an instance.

        params: mapping of .PARAM(value) or parameter name to value
        conns: mapping of port_name to signal
        """
        self.instances.append((module, inst_name, params, conns))

    def _render_parameters(self) -> str:
        if not self.parameters:
            return ""
        parts = []
        for name, default in self.parameters:
            if default is None:
                parts.append(name)
            else:
                parts.append(f"{name} = {default}")
        return f"#( {', '.join(parts)} )"

    def _render_ports(self) -> str:
        if not self.ports:
            return ""
        parts = []
        for name, direction, width in self.ports:
            parts.append(f"{direction} {_width_str(width)}{name}".strip())
        return "(\n    " + ",\n    ".join(parts) + "\n)"

    def _render_wires(self) -> List[str]:
        lines = []
        for name, width in self.wires:
            lines.append(f"wire {_width_str(width)}{name};".strip())
        return lines

    def _render_regs(self) -> List[str]:
        lines = []
        for name, width in self.regs:
            lines.append(f"reg {_width_str(width)}{name};".strip())
        return lines

    def _render_assigns(self) -> List[str]:
        return [f"assign {l} = {r};" for l, r in self.assigns]

    def _render_instances(self) -> List[str]:
        lines: List[str] = []
        for module, inst_name, params, conns in self.instances:
            param_str = ""
            if params:
                pairs = [f".{k}({v})" for k, v in params.items()]
                param_str = " #(" + ", ".join(pairs) + ")"
            conn_pairs = [f".{p}({s})" for p, s in conns.items()]
            lines.append(f"{module}{param_str} {inst_name} (" + ", ".join(conn_pairs) + ");")
        return lines

    def _render_always(self) -> List[str]:
        lines: List[str] = []
        for sens, body in self.always_blocks:
            lines.append(f"always @({sens}) begin")
            for bl in body:
                lines.append("    " + bl)
            lines.append("end")
        return lines

    def render(self) -> str:
        out: List[str] = []
        params = self._render_parameters()
        ports = self._render_ports()
        header = f"module {self.name} {params} {ports};".replace("  ", " ")
        out.append(header)

        # declarations
        out.extend(self._render_wires())
        out.extend(self._render_regs())
        if self.wires or self.regs:
            out.append("")

        # assigns
        out.extend(self._render_assigns())
        if self.assigns:
            out.append("")

        # instances
        out.extend(self._render_instances())
        if self.instances:
            out.append("")

        # always blocks
        out.extend(self._render_always())

        out.append(f"endmodule // {self.name}")
        return "\n".join(out)

    def write(self, filepath: str, encoding: str = "utf-8") -> None:
        text = self.render()
        with open(filepath, "w", encoding=encoding, newline="\n") as f:
            f.write(text)


__all__ = ["VerilogModule"]
