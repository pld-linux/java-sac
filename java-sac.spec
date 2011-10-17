Summary:	Java standard interface for CSS parser
Name:		sac
Version:	1.3
Release:	0.1
License:	W3C
Group:		Libraries
Source0:	http://www.w3.org/2002/06/%{name}java-%{version}.zip
# Source0-md5:	91c083636dc1a926bcb5b0bd0bde9ea5
Source1:	%{name}-build.xml
Source2:	%{name}-MANIFEST.MF
Source3:	http://mirrors.ibiblio.org/pub/mirrors/maven2/org/w3c/css/sac/1.3/%{name}-%{version}.pom
# Source3-md5:	2bebc9f4103026c9091d4bc7516f0daf
URL:		http://www.w3.org/Style/CSS/SAC/
BuildRequires:	ant
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	zip
Requires:	java
Requires:	jpackage-utils
BuildArch:	noarch

%description
SAC is a standard interface for CSS parsers, intended to work with
CSS1, CSS2, CSS3 and other CSS derived languages.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Languages/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
install -m 644 %{SOURCE1} build.xml
find . -name "*.jar" -exec rm -f {} \;

%build
%ant jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

# inject OSGi manifests
install -d META-INF
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/lib/sac.jar META-INF/MANIFEST.MF

install -d $RPM_BUILD_ROOT%{_javadir}
cp -p ./build/lib/sac.jar $RPM_BUILD_ROOT%{_javadir}/sac.jar

install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr build/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

#%%add_to_maven_depmap org.w3c.css sac %{version} JPP sac

# poms
#install -d $RPM_BUILD_ROOT%{_mavenpomdir}
#install -pm 644 %{SOURCE3} \
#    $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

#%post
#%%update_maven_depmap

#%postun
#%%update_maven_depmap

%files
%defattr(644,root,root,755)
%doc COPYRIGHT.html
%{_javadir}/%{name}.jar
#%{_mavenpomdir}/*
#%{_mavendepmapfragdir}/*

%files javadoc
%defattr(644,root,root,755)
%doc COPYRIGHT.html
%{_javadocdir}/%{name}
