%define git_repo xapian
%define oname xapian-core
%define with_php 0
%define with_mono 0

%define major 22
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Open Source Search Engine Library
Name:           xapian
Version:	%git_get_ver
Release:	%mkrel %git_get_rel
License:	GPLv2+
Group:		Databases
URL:		http://www.xapian.org/
Source:		%git_bs_source %{name}-%{version}.tar.gz
BuildRequires:	zlib-devel libuuid-devel


%description
Xapian is an Open Source Search Engine Library, released under the 
GPL. It's written in C++, with bindings to allow use from Perl, 
Python, PHP, Java, Tcl, C#, and Ruby (so far!)

Xapian is a highly adaptable toolkit which allows developers to easily
add advanced indexing and search facilities to their own applications. 
It supports the Probabilistic Information Retrieval model and also 
supports a rich set of boolean query operators.

%package bindings
Summary:	Bindings for the Xapian
License:	GPLv2+
Group:		Development/Other
BuildRequires:  swig
BuildRequires:	python-devel
%if %with_php
BuildRequires:	php-devel
BuildRequires:	php-cli
%endif

%description bindings
SWIG and JNI bindings allowing Xapian to be used from various 
other programming languages.

%package bindings-java
Summary:	Files needed for developing Java applications which use Xapian
Group:		Development/Java
Requires:	xapian >= %{version}
Requires:	java
BuildRequires:	java-rpmbuild

%description bindings-java
This package provides the files needed for developing Java applications which
use Xapian.

%if %with_mono
%package bindings-mono
Summary:	Files needed for developing C# applications which use Xapian
Group:		Development/Other
Requires:	xapian >= %{version}
Requires:	mono
BuildRequires:	mono-devel

%description bindings-mono
This package provides the files needed for developing 
C# applications which use Xapian.
%endif

%if %with_php
%package bindings-php
Summary:	Files needed for developing PHP scripts which use Xapian
Group:		Development/PHP
Requires:	xapian >= %{version}
Requires:	php

%description bindings-php
This package provides the files needed for developing 
PHP scripts which use Xapian.
%endif

%package bindings-python
Summary:	Files needed for developing Python scripts which use Xapian
Group:		Development/Python
Requires:	xapian >= %{version}
Requires:	python >= 2.5

%description bindings-python
This package provides the files needed for developing 
Python scripts which use Xapian.

%package bindings-ruby
Summary:	Files needed for developing Ruby applications which use Xapian
Group:		Development/Ruby
Requires:	xapian >= %{version}
Requires:	ruby
BuildRequires:	ruby-devel

%description bindings-ruby
This package provides the files needed for developing 
Ruby applications which use Xapian.

%package bindings-tcl
Summary:	Files needed for developing TCL scripts which use Xapian
Group:		Development/Other
Requires:	xapian >= %{version}
Requires:	tcl
BuildRequires:	tcl-devel


%description bindings-tcl
This package provides the files needed for developing 
TCL scripts which use Xapian.

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		Development/Other
Obsoletes:	%mklibname %{name} 14

%description -n %{libname}
Libraries for %{name}.

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

%prep
%git_get_source
%setup -q

%build
pushd xapian-core
	./preautoreconf
	autoreconf --install --force
	%configure2_5x --enable-maintainer-mode
	%make
popd

pushd xapian-bindings
	echo "aaa"
	mkdir -p m4
	cp -f ../xapian-core/m4-macros/xapian.m4 m4/
	autoreconf --install --force
# (tpg) do not check for this, to much effort to provide a patch
	%define Werror_cflags %nil

# We want to avoid using jni.h from libgcj-devel, so we force
# the includedir instead of using ./configure detection, which would
# default to libgcj jni.h:
# - Anssi (12/2007)
	export CPPFLAGS="%{optflags} -I%{java_home}/include"
	export JDK_HOME=%{java_home}
	export TCL_LIB=%{tcl_sitearch}
	autoreconf -fiv
	%configure2_5x \
	%if %with_mono
		--with-csharp \
	%endif
	%if %with_php
		--with-php \
	%endif
		--with-python \
		--with-ruby \
		--with-tcl \
		--with-java \
		--enable-maintainer-mode \
		XAPIAN_CONFIG=`pwd`/../xapian-core/xapian-config

	%make
popd


%install
pushd xapian-core
	%makeinstall_std
popd

pushd xapian-bindings
	%makeinstall_std

# Move to a proper location
	install -d -m755 %{buildroot}%{_libdir}
	mv %{buildroot}%{_builddir}/%{name}-%{version}/xapian-bindings/java/built/libxapian_jni.so %{buildroot}%{_libdir}

# Install the needed jar file as well
	install -d -m755 %{buildroot}%{_jnidir}
	install -m644 java/built/xapian_jni.jar %{buildroot}%{_jnidir}
popd

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

%files -n %{libname}
%{_libdir}/libxapian.so.%{major}*

%files bindings-java
%{_libdir}/libxapian_jni.so
%{_jnidir}/xapian_jni.jar

%if %with_mono
%files bindings-mono
%doc %{_docdir}/xapian-bindings/csharp
%{_libdir}/_XapianSharp.so
%{_libdir}/mono/XapianSharp/XapianSharp.dll
%{_libdir}/mono/gac/XapianSharp/%{version}*/XapianSharp.dll
%endif

%if %with_php
%files bindings-php
%doc %{_docdir}/xapian-bindings/php
%{_libdir}/php/extensions/xapian.so
%{_datadir}/php5/xapian.php
%endif

%files bindings-python
%doc %{_docdir}/xapian-bindings/python
%{python_sitearch}/xapian/*.py*
%{python_sitearch}/xapian/*.so

%files bindings-ruby
%doc %{_docdir}/xapian-bindings/ruby
%{ruby_sitearchdir}/_xapian.so
%{ruby_sitelibdir}/xapian.rb

%files bindings-tcl
%doc %{_docdir}/xapian-bindings/tcl8
%{tcl_sitearch}/xapian%{version}/*


%changelog -f %{_sourcedir}/%{name}-changelog.gitrpm.txt