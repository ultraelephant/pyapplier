# README

.scrobbler.log (Rockbox offline last.fm scrobling format) submiter.

# Features

  - .scrobbler.log submiting
  - multiple accounts support

# Requirenments

 - python3
 - python-pylast
 - python-setuptools
 - python-pyaml

# How to

#### Submit

```pyapplier.py -f /path/to/.scrobbler.log```

Some regions may have sync lag for last.fm website, so you may add ```-w``` flag for wait countdown.

Add ```-y``` flag to assume **Yes**. In case of multiple saved accounts add ```-y USERNAME``` 

#### Accounts mangment

Credetial stores in ```~/.config/pyapplier/saved_creds```

**list saved accounts**: ```pyapplier.py creds list```
**change account password**: ```pyapplier.py creds edit USERNAME```
**delete account**: ```pyapplier.py del USERNAME```
**add account**: ```pyapplier.py add USERNAME```

# Todo

 - prepare AUR installation Manifes
 - submit to AUR
