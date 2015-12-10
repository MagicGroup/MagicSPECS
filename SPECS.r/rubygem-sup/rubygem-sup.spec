%global gem_name sup

Summary: A console-based email client written in ruby
Name: rubygem-%{gem_name}
Version: 0.21.0
Release: 6%{?dist}
Group: Applications/Internet
License: GPLv2+
URL: http://sup.rubyforge.org/
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
Patch0: mkrf_conf.patch
# Revert dependency on ncursesw. The downside is incorrect wide character support.
# TODO: Resurrect rubygem-ncursesw (rhbz#597709).
# https://github.com/sup-heliotrope/sup/commit/c52016368e0456baf1ee97d25304b703da542cec
Patch1: rubygem-sup-Revert-Remove-all-ncursesw-warnings-since-it-s-a-har.patch

Requires: ruby(ncurses)
Requires: xapian-bindings-ruby

BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: xapian-core-devel
BuildRequires: rubygems-devel
BuildRequires: ncurses-devel
BuildRequires: xapian-bindings-ruby
BuildRequires: zlib-devel
BuildRequires: rubygem-rake
BuildRequires: gcc-c++

BuildArch: noarch

Provides: %{gem_name} = %{version}

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%description
Sup is a console-based email client for people with a lot of email. It
supports tagging, very fast full-text search, automatic contact-list
management, and more. If you're the type of person who treats email as an
extension of your long-term memory, Sup is for you.  Sup makes it easy to: -
Handle massive amounts of email.  - Mix email from different sources: mbox
files (even across different machines), Maildir directories, IMAP folders, POP
accounts, and GMail accounts.  - Instantaneously search over your entire email
collection. Search over body text, or use a query language to combine search
predicates in any way.  - Handle multiple accounts. Replying to email sent to
a particular account will use the correct SMTP server, signature, and from
address.  - Add custom code to handle certain types of messages or to handle
certain types of text within messages.  - Organize email with user-defined
labels, automatically track recent contacts, and much more!  The goal of Sup
is to become the email client of choice for nerds everywhere.


%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%patch0 -p1
%patch1 -p1

# Relax rubygem-chronic dependency.
sed -i '/chronic/ s/0.9.1/0.9/' %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install
rm %{_builddir}/%{gem_name}-%{version}%{gem_dir}/gems/%{gem_name}-%{version}/.gitignore
rm %{_builddir}/%{gem_name}-%{version}%{gem_dir}/gems/%{gem_name}-%{version}/.travis.yml
rm %{_builddir}/%{gem_name}-%{version}%{gem_dir}/gems/%{gem_name}-%{version}/.gitmodules
rm -fr %{_builddir}/%{gem_name}-%{version}%{gem_dir}/gems/%{gem_name}-%{version}/test
rm -fr %{_builddir}/%{gem_name}-%{version}%{gem_dir}/gems/%{gem_name}-%{version}/devel


%install
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}%{_bindir}
mv .%{gem_dir}/* %{buildroot}%{gem_dir}
mv .%{_bindir}/* %{buildroot}%{_bindir}

# Modifying gemspec to remove dependency on xapian-full and ncursesw

pushd %{buildroot}%{gem_dir}/specifications
sed -i -e '/xapian-full/, 1d' %{gem_name}-%{version}.gemspec
sed -i -e '/ncursesw/, 1d' %{gem_name}-%{version}.gemspec
popd

%files
%dir %{gem_instdir}
%{_bindir}/sup
%{_bindir}/sup-add
%{_bindir}/sup-config
%{_bindir}/sup-dump
%{_bindir}/sup-recover-sources
%{_bindir}/sup-sync
%{_bindir}/sup-tweak-labels
%{_bindir}/sup-import-dump
%{_bindir}/sup-psych-ify-config-files
%{_bindir}/sup-sync-back-maildir
%{gem_instdir}/*
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.21.0-6
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.21.0-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.21.0-4
- 为 Magic 3.0 重建

* Wed Sep 02 2015 Vít Ondruch <vondruch@redhat.com> - 0.21.0-3
- Relax rubygem-chronic dependency.
- Temporary use ncurses, until rubygem-ncursesw is in Fedora.
- Small cleanup.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 01 2015 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 0.21.0-1
- Add new source tarball and updated dependecies

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.10.2-11
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 0.10.2-8
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jun 14 2010 Shreyank Gupta <sgupta@redhat.com> - 0.10.2-5
- Added Provides: rubygem(%%{gemname}) = %%{version}

* Mon Jun 14 2010 Shreyank Gupta <sgupta@redhat.com> - 0.10.2-4
- Removed redundant versions from Requires.
- Moving %%{gemdir}/bin/* to %%{_bindir}
- Excluded lib/ncurses.rb
- Renamed package to rubygem-sup

* Fri Jun 11 2010 Shreyank Gupta <sgupta@redhat.com> - 0.10.2-3
- Removed require 'xapian-full' and 'ncursesw' from gemspec

* Wed Jun 09 2010 Shreyank Gupta <sgupta@redhat.com> - 0.10.2-2
- Moving %%geminstdir/bin/* instead of %%gemdir/bin/* to %%_bindir
- Requires xapian-bindings-ruby

* Mon Jun 07 2010 Shreyank Gupta <sgupta@redhat.com> - 0.10.2-1
- Initial package
