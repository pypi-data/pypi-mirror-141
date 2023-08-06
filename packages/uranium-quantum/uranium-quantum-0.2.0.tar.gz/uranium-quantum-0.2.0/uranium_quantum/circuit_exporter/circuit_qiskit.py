import numpy as np
from qiskit import QuantumRegister
from qiskit.circuit import ClassicalRegister
from qiskit import QuantumCircuit

from qiskit.circuit.library.standard_gates import XGate, YGate, ZGate, HGate
from qiskit.circuit.library import RXGate, RYGate, RZGate
from qiskit.circuit.library import RXXGate, RYYGate, RZZGate
from qiskit.circuit.library import RZXGate
from qiskit.circuit.library import SXGate, SXdgGate
from qiskit.circuit.library import SGate, SdgGate, TGate, TdgGate
from qiskit.circuit.library import UGate, U1Gate
from qiskit.circuit.library import SwapGate, iSwapGate
from uranium_quantum.circuit_exporter.qiskit_custom_gates import *

cr = ClassicalRegister(20)
qr = QuantumRegister(20)
qc = QuantumCircuit(qr, cr)

qc.u(1.57, 1.57, 1.57, qr[1])

qc.u(np.pi/2, 1.57, 1.57, qr[2])

qc.p(1.57, qr[3])

qc.id(qr[4])

qc.h(qr[5])

qc.unitary(hadamard_xy(), [6], label='hadamard-xy')

qc.unitary(hadamard_yz(), [7], label='hadamard-yz')

qc.h(qr[8])

qc.x(qr[9])

qc.y(qr[10])

qc.z(qr[11])

qc.unitary(pauli_x_root(2.0), [12], label='pauli-x-root')

qc.unitary(pauli_y_root((2**7.0)), [13], label='pauli-y-root')

qc.unitary(pauli_z_root((2**22.0)), [14], label='pauli-z-root')

qc.unitary(pauli_x_root_dagger((2**29.0)), [15], label='pauli-x-root-dagger')

qc.unitary(pauli_y_root_dagger((2**8.0)), [16], label='pauli-y-root-dagger')

qc.unitary(pauli_z_root_dagger(1.1), [17], label='pauli-z-root-dagger')

qc.rx(1.57, qr[18])

qc.ry(1.57, qr[19])

qc.unitary(c_dagger(), [0], label='c-dagger')

qc.p(0.5, qr[1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(UGate(1.57, 1.57, 1.57).control(num_ctrl_qubits=2, ctrl_state='01'), [qr[0], qr[1], qr[2]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.rz(1.57, qr[5])

qc.t(qr[6])

qc.tdg(qr[7])

qc.s(qr[8])

qc.sdg(qr[9])

qc.append(SXGate(), [qr[10]])

qc.append(SXdgGate(), [qr[11]])

qc.unitary(h(), [12], label='h')

qc.unitary(h_dagger(), [13], label='h-dagger')

qc.unitary(c(), [14], label='c')

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(UGate(1.5707963267948966, 1.57, 1.57).control(num_ctrl_qubits=2, ctrl_state='01'), [qr[0], qr[1], qr[3]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(U1Gate(1.57).control(num_ctrl_qubits=2, ctrl_state='01'), [qr[0], qr[1], qr[4]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(HGate().control(num_ctrl_qubits=2, ctrl_state='01'), [qr[0], qr[1], qr[5]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(hadamard_xy().control(num_ctrl_qubits=2, ctrl_state='01', label='hadamard-xy'), [qr[0], qr[1], qr[6]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(hadamard_yz().control(num_ctrl_qubits=2, ctrl_state='01', label='hadamard-yz'), [qr[0], qr[1], qr[7]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(HGate().control(num_ctrl_qubits=2, ctrl_state='01'), [qr[0], qr[1], qr[8]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(XGate().control(num_ctrl_qubits=2, ctrl_state='01'), [qr[0], qr[1], qr[8]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(YGate().control(num_ctrl_qubits=2, ctrl_state='01'), [qr[0], qr[1], qr[8]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(ZGate().control(num_ctrl_qubits=2, ctrl_state='01'), [qr[0], qr[1], qr[9]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(pauli_x_root(2.0).control(num_ctrl_qubits=2, ctrl_state='01', label='pauli-x-root'), [qr[0], qr[1], qr[8]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(pauli_y_root((2**7)).control(num_ctrl_qubits=2, ctrl_state='01', label='pauli-y-root'), [qr[0], qr[1], qr[9]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(pauli_z_root((2**22)).control(num_ctrl_qubits=2, ctrl_state='01', label='pauli-z-root'), [qr[0], qr[1], qr[8]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(pauli_x_root_dagger((2**29)).control(num_ctrl_qubits=2, ctrl_state='01', label='pauli-x-root-dagger'), [qr[0], qr[1], qr[9]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(pauli_y_root_dagger((2**8)).control(num_ctrl_qubits=2, ctrl_state='01', label='pauli-y-root-dagger'), [qr[0], qr[1], qr[6]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(pauli_z_root_dagger(1.1).control(num_ctrl_qubits=2, ctrl_state='01', label='pauli-z-root-dagger'), [qr[0], qr[1], qr[8]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(RXGate(1.57).control(num_ctrl_qubits=2, ctrl_state='01'), [qr[0], qr[1], qr[8]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(RYGate(1.57).control(num_ctrl_qubits=2, ctrl_state='01'), [qr[0], qr[1], qr[8]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.h(qr[1])
qc.append(RZGate(1.57).control(num_ctrl_qubits=2, ctrl_state='11'), [qr[0], qr[1], qr[10]])
qc.h(qr[1])

qc.h(qr[1])
qc.append(TGate().control(num_ctrl_qubits=2, ctrl_state='11'), [qr[0], qr[1], qr[9]])
qc.h(qr[1])

qc.h(qr[1])
qc.append(TdgGate().control(num_ctrl_qubits=2, ctrl_state='11'), [qr[0], qr[1], qr[17]])
qc.h(qr[1])

qc.h(qr[1])
qc.append(SGate().control(num_ctrl_qubits=2, ctrl_state='11'), [qr[0], qr[1], qr[13]])
qc.h(qr[1])

qc.h(qr[1])
qc.append(SdgGate().control(num_ctrl_qubits=2, ctrl_state='11'), [qr[0], qr[1], qr[15]])
qc.h(qr[1])

qc.h(qr[1])
qc.append(SXGate().control(num_ctrl_qubits=2, ctrl_state='11'), [qr[0], qr[1], qr[14]])
qc.h(qr[1])

qc.h(qr[1])
qc.append(SXdgGate().control(num_ctrl_qubits=2, ctrl_state='11'), [qr[0], qr[1], qr[16]])
qc.h(qr[1])

qc.h(qr[1])
qc.append(h().control(num_ctrl_qubits=2, ctrl_state='11', label='h'), [qr[0], qr[1], qr[15]])
qc.h(qr[1])

qc.h(qr[1])
qc.append(h_dagger().control(num_ctrl_qubits=2, ctrl_state='11', label='h-dagger'), [qr[0], qr[1], qr[16]])
qc.h(qr[1])

qc.h(qr[1])
qc.append(c().control(num_ctrl_qubits=2, ctrl_state='11', label='c'), [qr[0], qr[1], qr[15]])
qc.h(qr[1])

qc.h(qr[1])
qc.append(c_dagger().control(num_ctrl_qubits=2, ctrl_state='11', label='c-dagger'), [qr[0], qr[1], qr[2]])
qc.h(qr[1])

qc.append(RYYGate(0.22), [qr[6], qr[7]])

qc.append(RZZGate(0.22), [qr[8], qr[9]])

qc.append(xy(0.22, label='xy'), [qr[10], qr[11]])

qc.append(molmer_sorensen(label='molmer-sorensen'), [qr[12], qr[13]])

qc.h(qr[1])
qc.append(U1Gate(0.2).control(num_ctrl_qubits=2, ctrl_state='11'), [qr[0], qr[1], qr[3]])
qc.h(qr[1])

qc.swap(qr[0], qr[1])

qc.append(sqrt_swap(label='sqrt-swap'), [qr[2], qr[3]])

qc.append(sqrt_swap_dagger(label='sqrt-swap-dagger'), [qr[4], qr[5]])

qc.append(swap_theta(1.1, label='swap-theta'), [qr[6], qr[7]])

qc.iswap(qr[8], qr[9])

qc.append(fswap(label='fswap'), [qr[10], qr[11]])

qc.append(swap_root(2.1, label='swap-root'), [qr[12], qr[13]])

qc.append(swap_root_dagger(2.1, label='swap-root-dagger'), [qr[14], qr[15]])

qc.append(RXXGate(0.22), [qr[16], qr[17]])

qc.append(molmer_sorensen_dagger(label='molmer-sorensen-dagger'), [qr[0], qr[1]])

qc.append(berkeley(label='berkeley'), [qr[2], qr[3]])

qc.append(berkeley_dagger(label='berkeley-dagger'), [qr[4], qr[5]])

qc.append(ecp(label='ecp'), [qr[6], qr[7]])

qc.append(ecp_dagger(label='ecp-dagger'), [qr[8], qr[9]])

qc.append(w(label='w'), [qr[10], qr[11]])

qc.append(a(1.22, 1.44, label='a'), [qr[12], qr[13]])

qc.append(magic(label='magic'), [qr[14], qr[15]])

qc.append(magic_dagger(label='magic-dagger'), [qr[16], qr[17]])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(SwapGate().control(num_ctrl_qubits=2, ctrl_state='10'), [qr[0], qr[1], qr[3], qr[4]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.append(RZXGate(0.1), [qr[10], qr[11]])

qc.append(RZXGate(-0.2), [qr[12], qr[13]])

qc.append(givens(2.1, label='givens'), [qr[14], qr[15]])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(sqrt_swap().control(num_ctrl_qubits=2, ctrl_state='10', label='sqrt-swap'), [qr[0], qr[1], qr[3], qr[4]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(sqrt_swap_dagger().control(num_ctrl_qubits=2, ctrl_state='10', label='sqrt-swap-dagger'), [qr[0], qr[1], qr[3], qr[4]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(swap_theta(1.2).control(num_ctrl_qubits=2, ctrl_state='10', label='swap-theta'), [qr[0], qr[1], qr[3], qr[4]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(iSwapGate().control(num_ctrl_qubits=2, ctrl_state='10'), [qr[0], qr[1], qr[3], qr[4]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(fswap().control(num_ctrl_qubits=2, ctrl_state='10', label='fswap'), [qr[0], qr[1], qr[3], qr[4]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(swap_root(2).control(num_ctrl_qubits=2, ctrl_state='10', label='swap-root'), [qr[0], qr[1], qr[3], qr[4]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(swap_root_dagger(3).control(num_ctrl_qubits=2, ctrl_state='10', label='swap-root-dagger'), [qr[0], qr[1], qr[3], qr[4]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(RXXGate(0.1).control(num_ctrl_qubits=2, ctrl_state='10'), [qr[0], qr[1], qr[3], qr[4]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(RYYGate(0.1).control(num_ctrl_qubits=2, ctrl_state='10'), [qr[0], qr[1], qr[3], qr[4]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(RZZGate(0.1).control(num_ctrl_qubits=2, ctrl_state='10'), [qr[0], qr[1], qr[3], qr[4]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(xy(0.1).control(num_ctrl_qubits=2, ctrl_state='10', label='xy'), [qr[0], qr[1], qr[3], qr[4]])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.h(qr[1])
qc.append(molmer_sorensen().control(num_ctrl_qubits=2, ctrl_state='10', label='molmer-sorensen'), [qr[0], qr[1], qr[3], qr[4]])
qc.h(qr[1])

qc.h(qr[1])
qc.append(molmer_sorensen_dagger().control(num_ctrl_qubits=2, ctrl_state='10', label='molmer-sorensen-dagger'), [qr[0], qr[1], qr[3], qr[4]])
qc.h(qr[1])

qc.h(qr[1])
qc.append(berkeley().control(num_ctrl_qubits=2, ctrl_state='10', label='berkeley'), [qr[0], qr[1], qr[3], qr[4]])
qc.h(qr[1])

qc.h(qr[0])
qc.h(qr[1])
qc.append(berkeley_dagger().control(num_ctrl_qubits=2, ctrl_state='11', label='berkeley-dagger'), [qr[0], qr[1], qr[3], qr[4]])
qc.h(qr[0])
qc.h(qr[1])

qc.h(qr[1])
qc.append(ecp().control(num_ctrl_qubits=2, ctrl_state='10', label='ecp'), [qr[0], qr[1], qr[3], qr[4]])
qc.h(qr[1])

qc.h(qr[0])
qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(ecp_dagger().control(num_ctrl_qubits=2, ctrl_state='10', label='ecp-dagger'), [qr[0], qr[1], qr[3], qr[4]])
qc.h(qr[0])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.h(qr[1])
qc.append(w().control(num_ctrl_qubits=2, ctrl_state='10', label='w'), [qr[0], qr[1], qr[3], qr[4]])
qc.h(qr[1])

qc.h(qr[1])
qc.append(a(0.1, 0.2).control(num_ctrl_qubits=2, ctrl_state='10', label='a'), [qr[0], qr[1], qr[3], qr[4]])
qc.h(qr[1])

qc.h(qr[0])
qc.h(qr[1])
qc.append(magic().control(num_ctrl_qubits=2, ctrl_state='00', label='magic'), [qr[0], qr[1], qr[3], qr[4]])
qc.h(qr[0])
qc.h(qr[1])

qc.h(qr[0])
qc.h(qr[1])
qc.append(magic_dagger().control(num_ctrl_qubits=2, ctrl_state='10', label='magic-dagger'), [qr[0], qr[1], qr[3], qr[4]])
qc.h(qr[0])
qc.h(qr[1])

qc.h(qr[0])
qc.h(qr[1])
qc.append(RZXGate(0.1).control(num_ctrl_qubits=2, ctrl_state='10', label='cross-resonance'), [qr[0], qr[1], qr[3], qr[4]])
qc.h(qr[0])
qc.h(qr[1])

qc.h(qr[0])
qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(RZXGate(-0.1).control(num_ctrl_qubits=2, ctrl_state='01', label='cross-resonance-dg'), [qr[0], qr[1], qr[3], qr[4]])
qc.h(qr[0])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.h(qr[0])
qc.unitary(gate_rotation_to_y_basis(), [1])
qc.append(givens(0.1).control(num_ctrl_qubits=2, ctrl_state='01', label='givens'), [qr[0], qr[1], qr[3], qr[4]])
qc.h(qr[0])
qc.unitary(gate_undo_rotation_to_y_basis(), [1])

qc.measure(0, 0)

qc.measure(1, 1)

qc.measure(2, 2)

qc.measure(3, 3)

qc.measure(4, 4)

qc.measure(5, 5)

qc.measure(6, 6)

qc.measure(7, 7)

qc.measure(8, 8)

qc.measure(9, 9)

qc.measure(10, 10)

qc.measure(11, 11)

qc.measure(12, 12)

qc.measure(13, 13)

qc.measure(14, 14)

qc.measure(15, 15)

qc.measure(16, 16)

qc.measure(17, 17)

qc.measure(18, 18)

qc.measure(19, 19)

