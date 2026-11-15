# Third-party source notices

The `cball_ext/` directory contains Ball-related C source and local wrappers.
The original author and copyright comments have been retained. In particular,
`utilities.c` declares copyright 2017 ChengFeng Liu and Jin Zhu and permission
under GNU GPL version 3 or, at the recipient's option, any later version.

The GNU GPL v3 text is included in [COPYING.GPL-3.0.txt](COPYING.GPL-3.0.txt),
obtained from <https://www.gnu.org/licenses/gpl-3.0.txt>.

The repository root contains an MIT license for the project's original code.
Third-party source retains its existing notices and applicable license terms.
The included GPL text documents the Ball source notice and does not attribute
all project files to the Ball authors.

Background:

- Pan et al., *Ball Covariance: A Generic Measure of Dependence in Banach Space*:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC7720858/>.
- The C functions `bdd_matrix_bias`, distance/rank utilities, and median helpers
  are retained with their source comments; `snp_bcov.c` supplies the project's
  SNP-specialised statistic and rank interface.

## Imported original implementation

`Original_Implementation/` preserves the source snapshot from
<https://github.com/chuangli66/RWSPM>. See its
[import provenance](Original_Implementation/IMPORT_PROVENANCE.md) for the exact
commit, attribution and licensing scope. The imported snapshot has no top-level
LICENSE file. Its third-party code, packages and documents retain their
respective notices and require separate consideration of applicable permissions.
