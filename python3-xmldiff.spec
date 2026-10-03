#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Create diffs of XML files
Summary(pl.UTF-8):	Tworzenie diffów plików XML
Name:		python3-xmldiff
Version:	3.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/xmldiff/
Source0:	https://files.pythonhosted.org/packages/source/x/xmldiff/xmldiff-%{version}.tar.gz
# Source0-md5:	9afc015892ff6993a97e0b481e0c69bd
URL:		https://pypi.org/project/xmldiff/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools >= 1:61.2
%if %{with tests}
BuildRequires:	python3-lxml >= 3.1.0
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-sphinx_argparse >= 0.2.2
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xmldiff is a library and a command-line utility for making diffs out
of XML. This may seem like something that doesn't need a dedicated
utility, but change detection in hierarchical data is very different
from change detection in flat data. XML type formats are also not only
used for computer readable data, it is also often used as a format for
hierarchical data that can be rendered into human readable formats. A
traditional diff on such a format would tell you line by line the
differences, but this would not be be readable by a human. xmldiff
provides tools to make human readable diffs in those situations.

%description -l pl.UTF-8
xmldiff to biblioteka i narzędzie linii poleceń do tworzenia
zestawienia różnic (diffów) danych XML. Może to nie wydawać się
zadaniem wymagającym dedykowanego narzędzia, ale wykrywanie zmian w
danych hierarchicznych różni się od wykrywania zmian w płaskich
danych. Formaty typu XML nie służą tylko do danych czytelnych dla
komputera, ale często są używane także jako format danych
hierarchicznych odwzorowywanych w formatach czytelnych dla ludzi.
Tradycyjny diff takiego formatu pokaże różnice linia po linii, ale nie
będzie to czytelne dla człowieka. xmldiff udostępnia narzędzia do
tworzenia diffów czytelnych dla człowieka w takich sytuacjach.

%package apidocs
Summary:	API documentation for Python xmldiff module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona xmldiff
Group:		Documentation

%description apidocs
API documentation for Python xmldiff module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona xmldiff.

%prep
%setup -q -n xmldiff-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/xmldiff
%attr(755,root,root) %{_bindir}/xmlpatch
%{py3_sitescriptdir}/xmldiff
%{py3_sitescriptdir}/xmldiff-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
