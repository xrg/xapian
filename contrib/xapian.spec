%define oname xapian-core
%define major 22
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Open Source Search Engine Library
Name:           xapian
Version:	1.2.12
Release:        %mkrel 1
License:	GPLv2+
Group:		Databases
URL:		http://www.xapian.org/
Source0:	http://www.oligarchy.co.uk/xapian/%{version}/%{oname}-%{version}.tar.gz
BuildRequires:	zlib-devel libuuid-devel

%description
Xapian is an Open Source Search Engine Library, released under the 
GPL. It's written in C++, with bindings to allow use from Perl, 
Python, PHP, Java, Tcl, C#, and Ruby (so far!)

Xapian is a highly adaptable toolkit which allows developers to easily
add advanced indexing and search facilities to their own applications. 
It supports the Probabilistic Information Retrieval model and also 
supports a rich set of boolean query operators.

%files
%{_bindir}/copydatabase
%{_bindir}/delve
%{_bindir}/quest
%{_bindir}/simpleexpand
%{_bindir}/simpleindex
%{_bindir}/simplesearch
%{_bindir}/xapian-compact
%{_bindir}/xapian-check
%{_bindir}/xapian-progsrv
%{_bindir}/xapian-tcpsrv
%{_bindir}/xapian-inspect
%{_bindir}/xapian-chert-update
%{_bindir}/xapian-metadata
%{_bindir}/xapian-replicate
%{_bindir}/xapian-replicate-server
%{_mandir}/man1/*

#--------------------------------------------------------------------

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		Development/Other
Obsoletes:	%mklibname %{name} 14

%description -n %{libname}
Libraries for %{name}.

%files -n %{libname}
%{_libdir}/libxapian.so.%{major}*

#--------------------------------------------------------------------

%package  -n %{develname}
Summary:	Development files for %{name}
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%mklibname %{name} 14 -d
Obsoletes:	%mklibname %{name} 15 -d

%description -n %{develname}
Header files for %{name}.

%files  -n %{develname}
%{_bindir}/xapian-config
%doc %{_docdir}/%{oname}/
%dir %{_includedir}/xapian
%{_includedir}/xapian/*.h
%{_includedir}/*.h
%{_datadir}/aclocal/xapian.m4
%{_libdir}/libxapian.so
%{_libdir}/cmake/xapian/xapian-config-version.cmake
%{_libdir}/cmake/xapian/xapian-config.cmake
%{_libdir}/libxapian.a 
%{_libdir}/libxapian.la

#--------------------------------------------------------------------

%prep
%setup -qn %{oname}-%{version}

%build
%configure2_5x

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

