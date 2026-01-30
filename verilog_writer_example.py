"""Example usage of verilog_writer.

Run with:

    python python_test1\verilog_writer_example.py

This will generate `dff.v` alongside this script.
"""
import os
from verilog_writer import VerilogModule


def main():
    m = VerilogModule("dff")
    m.add_port("clk", "input")
    m.add_port("rst", "input")
    m.add_port("d", "input", width=8)
    m.add_port("q", "output", width=8)

    # internal register
    m.add_reg("q_reg", width=8)

    # sequential logic
    m.add_always("posedge clk or posedge rst", [
        "if (rst) q_reg <= 0;",
        "else q_reg <= d;",
    ])

    # connect output
    m.add_assign("q", "q_reg")

    out_path = os.path.join(os.path.dirname(__file__), "dff.v")
    m.write(out_path)
    print("Wrote:", out_path)


if __name__ == "__main__":
    main()
