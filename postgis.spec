%define pg_version	%(rpm -q --queryformat '%{VERSION}' postgresql-backend-devel)
Summary:	Geographic Information Systems Extensions to PostgreSQL
Summary(pl.UTF-8):	Rozszerzenie do PostgreSQL wspomagające Geograficzne Systemy Informacyjne
Name:		postgis
Version:	1.3.2
Release:	1
License:	GPL v2
Group:		Applications/Databases
Source0:	http://postgis.refractions.net/download/%{name}-%{version}.tar.gz
# Source0-md5:	b0d52c2c23c316fc9884632a80b380a5
Patch0:		%{name}-geos.patch
URL:		http://postgis.refractions.net/
BuildRequires:	geos-devel >= 2.1.4
BuildRequires:	perl-base
BuildRequires:	postgresql-backend-devel >= 7.1
BuildRequires:	postgresql-devel >= 7.1
BuildRequires:	proj-devel
Requires:	postgresql-module-plpgsql = %{pg_version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# oh well... I also don't understand this... ;)

%description
This package contains a module which implements GIS simple features,
ties the features to rtree indexing, and provides some spatial
functions for accessing and analyzing geographic data.

%description -l pl.UTF-8
Pakiet ten zawiera moduł implementujący proste funkcje GIS, wiąże je z
indeksowaniem rtree oraz dostarcza funkcje dostępu oraz analizy danych
geograficznych.

%prep
%setup  -q
%patch0 -p1

%build
%configure \
	--with-geos \
	--with-geos-libdir=/usr/%{_lib} \
	--with-pgsql \
	--with-proj \
	--with-proj-libdir=/usr/%{_lib}

%{__make} liblwgeom loaderdumper utils \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags}" \
	LPATH="%{_libdir}/postgresql" \
	shlib="%{name}.so"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/postgresql,%{_bindir}}

%{__make} -C loader install \
	bindir="$RPM_BUILD_ROOT%{_bindir}" \
	INSTALL_PROGRAM=install

install lwgeom/%{name}.so $RPM_BUILD_ROOT%{_libdir}/postgresql

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS NEWS README.postgis TODO doc/html *.sql
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/postgresql/%{name}.so
