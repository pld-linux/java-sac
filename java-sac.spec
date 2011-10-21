#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		srcname	sac
Summary:	Java standard interface for CSS parser
Name:		java-%{srcname}
Version:	1.3
Release:	1
License:	W3C
Group:		Libraries/Java
Source0:	http://www.w3.org/2002/06/%{srcname}java-%{version}.zip
# Source0-md5:	91c083636dc1a926bcb5b0bd0bde9ea5
Source1:	build.xml
Source2:	MANIFEST.MF
URL:		http://www.w3.org/Style/CSS/SAC/
BuildRequires:	ant
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	zip
Requires:	java
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SAC is a standard interface for CSS parsers, intended to work with
CSS1, CSS2, CSS3 and other CSS derived languages.

%package javadoc
Summary:	Javadoc for SAC
Group:		Documentation

%description javadoc
Javadoc for SAC.

%prep
%setup -q -n %{srcname}-%{version}
cp -p %{SOURCE1} build.xml

find -name "*.jar" | xargs rm -v

%build
%ant jar %{?with_javadoc:javadoc}

# inject OSGi manifests
install -d META-INF
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/lib/sac.jar META-INF/MANIFEST.MF

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/sac.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -pr build/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc COPYRIGHT.html
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%doc COPYRIGHT.html
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
