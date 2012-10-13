%define with_php 0

Summary:	Bindings for the Xapian
Name:		xapian-bindings
Version:	1.2.12
Release:	%mkrel 1
License:	GPLv2+
Group:		Development/Other
URL:		http://www.xapian.org
Source0:	http://www.oligarchy.co.uk/xapian/%{version}/%{name}-%{version}.tar.gz
Patch0:		xapian-bindings-1.2.2-no-pyc.patch
Patch1:		xapian-bindings-1.2.3-linkage.patch
BuildRequires:	xapian-devel >= %{version}
BuildRequires:	python-devel
%if %with_php
BuildRequires:	php-devel
BuildRequires:	php-cli
%endif
BuildRequires:	tcl-devel
BuildRequires:	java-rpmbuild
BuildRequires:	ruby-devel
BuildRequires:	mono-devel

%description
SWIG and JNI bindings allowing Xapian to be used from various 
other programming languages.

%package java
Summary:	Files needed for developing Java applications which use Xapian
Group:		Development/Java
Requires:	xapian >= %{version}
Requires:	java

%description java
This package provides the files needed for developing Java applications which
use Xapian.

%package mono
Summary:	Files needed for developing C# applications which use Xapian
Group:		Development/Other
Requires:	xapian >= %{version}
Requires:	mono

%description mono
This package provides the files needed for developing 
C# applications which use Xapian.

%if %with_php
%package php
Summary:	Files needed for developing PHP scripts which use Xapian
Group:		Development/PHP
Requires:	xapian >= %{version}
Requires:	php

%description php
This package provides the files needed for developing 
PHP scripts which use Xapian.
%endif

%package python
Summary:	Files needed for developing Python scripts which use Xapian
Group:		Development/Python
Requires:	xapian >= %{version}
Requires:	python >= 2.5

%description python
This package provides the files needed for developing 
Python scripts which use Xapian.

%package ruby
Summary:	Files needed for developing Ruby applications which use Xapian
Group:		Development/Ruby
Requires:	xapian >= %{version}
Requires:	ruby

%description ruby
This package provides the files needed for developing 
Ruby applications which use Xapian.

%package tcl
Summary:	Files needed for developing TCL scripts which use Xapian
Group:		Development/Other
Requires:	xapian >= %{version}
Requires:	tcl

%description tcl
This package provides the files needed for developing 
TCL scripts which use Xapian.

%prep
%setup -q
%patch0 -p1
#%patch1 -p0 -b .link

%build
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
	--with-csharp \
%if %with_php
	--with-php \
%endif
	--with-python \
	--with-ruby \
	--with-tcl \
	--with-java

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

# Move to a proper location
install -d -m755 %{buildroot}%{_libdir}
mv %{buildroot}%{_builddir}/%{name}-%{version}/java/built/libxapian_jni.so %{buildroot}%{_libdir}

# Install the needed jar file as well
install -d -m755 %{buildroot}%{_jnidir}
install -m644 java/built/xapian_jni.jar %{buildroot}%{_jnidir}

%files java
%{_libdir}/libxapian_jni.so
%{_jnidir}/xapian_jni.jar

%files mono
%doc %{_docdir}/xapian-bindings/csharp
%{_libdir}/_XapianSharp.so
%{_libdir}/mono/XapianSharp/XapianSharp.dll
%{_libdir}/mono/gac/XapianSharp/%{version}*/XapianSharp.dll

%if %with_php
%files php
%doc %{_docdir}/xapian-bindings/php
%{_libdir}/php/extensions/xapian.so
%{_datadir}/php5/xapian.php
%endif

%files python
%doc %{_docdir}/xapian-bindings/python
%{python_sitearch}/xapian/*.py*
%{python_sitearch}/xapian/*.so

%files ruby
%doc %{_docdir}/xapian-bindings/ruby
%{ruby_sitearchdir}/_xapian.so
%{ruby_sitelibdir}/xapian.rb

%files tcl
%doc %{_docdir}/xapian-bindings/tcl8
%{tcl_sitearch}/xapian%{version}/*

