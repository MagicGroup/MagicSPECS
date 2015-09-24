%global	gem_name ditz

Summary:	A command-line issue tracker
Name:		rubygem-%{gem_name}
Version:	0.5
Release:	14%{?dist}
Group:		Applications/Productivity
License:	GPLv3+ with exceptions
URL:		http://ditz.rubyforge.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	rubygem(trollop)
Requires:	ruby(rubygems)
Requires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	rubygem(rake)
BuildRequires:	rubygem(hoe)
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
# available from following link or git repository for ditz project
Source1:	http://gitorious.org/ditz/mainline/blobs/raw/master/README.txt

%description
A command-line issue tracker written in ruby.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
cp -p %{SOURCE1} README.txt
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# replace /usr/bin/ruby1.8 by /usr/bin/ruby
pushd %{buildroot}%{gem_instdir}
sed -i 's|/usr/bin/ruby1.8|/usr/bin/ruby|' bin/ditz
popd

cd %{buildroot}/%{_bindir}
rm %{buildroot}/%{gem_libdir}/trollop.rb
rm -rf %{buildroot}/%{gem_docdir}/ri/Trollop
mkdir -p %{buildroot}/%{_mandir}/man1
cd %{buildroot}/%{_mandir}/man1
gzip %{buildroot}/%{gem_instdir}/man/ditz.1
ln -s ../../../../%{gem_instdir}/man/ditz.1 ditz.1

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%dir %{gem_instdir}/
%{gem_instdir}/bin
%{gem_instdir}/contrib
%{gem_instdir}/INSTALL
%{gem_libdir}
%{gem_instdir}/man
%{gem_instdir}/Manifest.txt
%{gem_instdir}/Rakefile
%{gem_instdir}/setup.rb
%{gem_instdir}/www
%doc %{gem_docdir}
%doc %{gem_instdir}/PLUGINS.txt
%doc %{gem_instdir}/README.txt
%doc %{gem_instdir}/Changelog
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/ReleaseNotes
%{gem_cache}
%{gem_spec}
%{_bindir}/%{gem_name}
%{_mandir}/man1/*

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 22 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.5-11
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 06 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.5-8
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 01 2009 jan.klepek@hp.com - 0.5-5
- fixed #532244, redundant ri doc for trollop removed

* Sun Oct 04 2009 Jan Klepek <jan.klepek@hp.com> - 0.5-4
- moved more files into %%doc

* Sat Oct 03 2009 Jan Klepek <jan.klepek@hp.com> - 0.5-3
- fixed duplicate files, fixed macros usage, changed license to "GPLv3+ with exceptions"

* Wed Sep 30 2009 Jan Klepek <jan.klepek@hp.com> - 0.5-2
- Added README from git repository with permission to link against trollop library

* Mon Sep 21 2009 Jan Klepek <jan.klepek@hp.com> - 0.5-1
- Change of maintainer, rpmlint warnings cleanup

* Sat Jan 24 2009 Kyle McMartin <kyle@redhat.com> - 0.5-0
- Initial release of ditz.
